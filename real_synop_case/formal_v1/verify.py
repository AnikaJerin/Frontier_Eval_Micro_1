import hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root));from grader import grade,parse
f=Path(__file__).parent;ref=json.loads((f/'reference.json').read_text());assert len(ref)==27
assert (f/'report.txt').read_text().strip() in (f/'prompt.txt').read_text()
assert grade(json.dumps(ref),ref)['passed'];checks=1
for k,v in ref.items():
 for mode in ('wrong','missing','bool','string','extra'):
  a=ref.copy()
  if mode=='wrong':a[k]=0 if v is None else v+1
  elif mode=='missing':del a[k]
  elif mode=='bool':a[k]=True
  elif mode=='string':a[k]=str(v)
  else:a['extra']=1
  assert not grade(json.dumps(a),ref)['passed'],(k,mode);checks+=1
for text in ('','[]','{}','{"x":NaN}','{"x":1,"x":1}','{} trailing'):
 assert not grade(text,ref)['passed'];checks+=1
for d,expected in ((0.0000005,True),(0.000002,False)):
 a=ref.copy();a['air_temperature_c']+=d;assert grade(json.dumps(a),ref)['passed']==expected;checks+=1
# Separate arithmetic cross-checks against explicit group values.
assert ref['air_temperature_c']==222/10 and ref['dewpoint_c']==210/10
assert ref['minimum_temperature_c']==213/10 and ref['pressure_change_24h_hpa']==-8/10 and ref['precipitation_24h_mm']==20/10
assert ref['station_pressure_hpa']==1000+87/10 and ref['msl_pressure_hpa']==1000+188/10
print(f'{len(ref)} fields; {checks} positive, mutation, schema and tolerance checks passed')
