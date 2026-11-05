"""Inventory source bytes and conservative candidate fields; no API or hidden data."""
import collections,datetime,hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parent

def run():
 data=(P/'raw/attributed_reports.jsonl').read_bytes(); lines=data.splitlines();rows=[]; invalid=[]
 for i,line in enumerate(lines,1):
  try:
   row=json.loads(line)
   if not isinstance(row,dict): raise ValueError('not an object')
   rows.append((i,row))
  except (ValueError,UnicodeError) as e:invalid.append({'line':i,'error':str(e)})
 keys=('format','observation_time_utc','original_source_url','raw','record_id','reference_status','sha256','source','station')
 seen=collections.Counter(r.get('raw') for _,r in rows);ids=collections.Counter(r.get('record_id') for _,r in rows)
 inventory=[]; candidates=[]
 for line,r in rows:
  raw=r.get('raw') or '';fmt=r.get('format');errors=[]; ts=r.get('observation_time_utc') or ''
  try:dt=datetime.datetime.strptime(ts,'%Y%m%d%H%M')
  except ValueError:
   dt=None
   if not re.fullmatch(r'\d{6}Z',ts):errors.append('invalid metadata timestamp')
  toks=raw.split(); expected={'SYNOP':'AAXX','METAR':'METAR','TAF':'TAF'}.get(fmt)
  if not expected or not toks or toks[0]!=expected:errors.append('format/header mismatch or unsupported format')
  if not raw or hashlib.sha256(raw.encode()).hexdigest()!=r.get('sha256'):errors.append('raw SHA-256 mismatch')
  if seen[raw]>1:errors.append('duplicate raw report')
  if ids[r.get('record_id')]>1:errors.append('duplicate record id')
  if any(not r.get(k) for k in keys if k!='original_source_url'):errors.append('missing required metadata')
  fields={}; issues=[]
  if fmt=='SYNOP' and len(toks)>=6 and toks[0]=='AAXX':
   if not re.fullmatch(r'\d{5}',toks[1]) or not re.fullmatch(r'\d{5}',toks[2]):errors.append('malformed SYNOP header')
   elif dt and (int(toks[1][:2])!=dt.day or int(toks[1][2:4])!=dt.hour):errors.append('time mismatch')
   if toks[2]!=r.get('station'):errors.append('station mismatch')
   groups=toks[5:];groups=groups[:groups.index('333')] if '333' in groups else groups
   matches=[g for g in groups if re.fullmatch(r'1[01]\d{3}',g)]
   if len(matches)==1:
    g=matches[0]; fields['air_temperature_c']=(-1 if g[1]=='1' else 1)*int(g[2:])/10
   else:issues.append('air temperature missing or ambiguous')
  elif fmt in ('METAR','TAF') and len(toks)>=4:
   m=re.match(r'^(?:METAR|TAF)\s+(?:(?:AMD|COR)\s+)?([A-Z]{4})\s+(\d{2})(\d{2})(\d{2})Z\b',raw)
   if not m:errors.append('unrecognized station/time header')
   else:
    if m.group(1)!=r.get('station'):errors.append('station mismatch')
    if dt and tuple(map(int,m.groups()[1:]))!=(dt.day,dt.hour,dt.minute):errors.append('time mismatch')
    if not dt and re.fullmatch(r'\d{6}Z',ts) and ts!=m.group(2)+m.group(3)+m.group(4)+'Z':errors.append('time mismatch')
   if fmt=='METAR':
                                                                                    
    body=re.split(r'\s(?:TEMPO|BECMG|NOSIG|RMK)\b',raw,1)[0]
    m=re.search(r'\b(M?\d{2})/(M?\d{2})\b',body)
    if m:
     conv=lambda x: -int(x[1:]) if x.startswith('M') else int(x)
     fields.update(air_temperature_c=conv(m.group(1)),dewpoint_c=conv(m.group(2)))
    else:issues.append('temperature/dewpoint group missing or unsupported')
   else:
    m=re.search(r'\b(\d{2})(\d{2})/(\d{2})(\d{2})\b',raw)
    if m:fields.update(valid_from_day=int(m[1]),valid_from_hour=int(m[2]),valid_to_day=int(m[3]),valid_to_hour=int(m[4]))
    else:issues.append('validity period missing or unsupported')
  elif fmt=='SYNOP' and len(toks)==4 and toks[3].rstrip('=')=='NIL':issues.append('NIL: no meteorological observation groups transmitted')
  else:errors.append('short or unsupported report')
  item={'record_id':r.get('record_id'),'format':fmt,'line':line,'structural_flags':errors,'field_flags':issues,'individual_source_url_missing':not bool(r.get('original_source_url')),'candidate_field_count':len(fields)}
  inventory.append(item)
  if fields and not errors:candidates.append({'record_id':r['record_id'],'format':fmt,'fields':fields,'status':'provisional_needs_independent_record_review'})
 out={'source_file_sha256':hashlib.sha256(data).hexdigest(),'lines':len(lines),'records':len(rows),'invalid_json_lines':invalid,'format_counts':dict(collections.Counter(r.get('format') for _,r in rows)),'unique_raw':len(seen),'unique_ids':len(ids),'records_with_flags':sum(bool(x['structural_flags']) for x in inventory),'flag_counts':dict(collections.Counter(e for x in inventory for e in x['structural_flags'])),'individual_source_urls_missing':sum(x['individual_source_url_missing'] for x in inventory),'candidate_records':len(candidates),'candidate_field_values':sum(len(c['fields']) for c in candidates),'candidate_format_counts':dict(collections.Counter(x['format'] for x in candidates)),'records':inventory}
 (P/'inventory.json').write_text(json.dumps(out,indent=2)+'\n');(P/'candidate_references.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in candidates))
 print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
if __name__=='__main__':run()
