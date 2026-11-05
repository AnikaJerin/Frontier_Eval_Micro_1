"""Local stdlib evaluation runner. Remote calls are only for model inference."""
import argparse,hashlib,json,math,os,random,time,urllib.request,urllib.error
from datetime import datetime,timezone
from pathlib import Path
from grader import grade
ROOT=Path(__file__).resolve().parent

def atomic(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp')
 with tmp.open('w') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 tmp.replace(path)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--model',required=True);p.add_argument('--provider',choices=('openai','meta'),default='openai');p.add_argument('--trials',type=int,default=3);p.add_argument('--max-output-tokens',type=int,default=2048);p.add_argument('--output',type=Path,default=ROOT/'new_results');p.add_argument('--input-usd-per-million',type=float);p.add_argument('--output-usd-per-million',type=float);p.add_argument('--cached-input-usd-per-million',type=float);a=p.parse_args()
 if a.trials<1 or a.max_output_tokens<16:p.error('trials must be positive and output cap at least 16')
 prices=[a.input_usd_per_million,a.output_usd_per_million,a.cached_input_usd_per_million]
 if any(x is not None for x in prices) and (not all(x is not None and math.isfinite(x) and x>=0 for x in prices)):p.error('supply all three finite nonnegative prices or none')
 key=os.environ.get('META_API_KEY' if a.provider=='meta' else 'OPENAI_API_KEY')
 if not key:raise SystemExit('Required API key not present in environment')
 tasks=[json.loads(f.read_text()) for f in sorted((ROOT/'data').glob('*.json'))]
 config={'model':a.model,'provider':a.provider,'trials':a.trials,'max_output_tokens':a.max_output_tokens,'prices':prices,'dataset_sha256':hashlib.sha256(json.dumps(tasks,sort_keys=True).encode()).hexdigest(),'grader_sha256':hashlib.sha256((ROOT/'grader.py').read_bytes()).hexdigest()}
 runid=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:16];folder=a.output/runid;folder.mkdir(parents=True,exist_ok=True);atomic(folder/'config.json',config)
 lock=folder/'run.lock'
 try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
 except FileExistsError:raise SystemExit('Run locked; verify no process is active before deleting run.lock')
 os.close(fd)
 try:
  records=[]
  for t in tasks:
   for n in range(1,a.trials+1):
    out=folder/f"{t['id']}_{n}.json"
    if out.exists():records.append(json.loads(out.read_text()));continue
    if a.provider=='meta':
     url='https://api.meta.ai/v1/chat/completions';payload={'model':a.model,'messages':[{'role':'user','content':t['model_visible_prompt']}],'reasoning_effort':'minimal','max_tokens':a.max_output_tokens}
    else:
     url='https://api.openai.com/v1/responses';payload={'model':a.model,'input':t['model_visible_prompt'],'max_output_tokens':a.max_output_tokens,'store':False}
    start=time.monotonic()
    for attempt in range(5):
     req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
     try:
      with urllib.request.urlopen(req,timeout=120) as stream:response=json.load(stream)
      break
     except urllib.error.HTTPError as e:
      if e.code not in (429,500,502,503,504) or attempt==4:raise SystemExit(f'API HTTP {e.code}')
      h=e.headers.get('Retry-After','') if e.headers else ''
      delay=min(60,float(h)) if h.replace('.','',1).isdigit() else min(60,2**attempt+random.random());time.sleep(max(0,delay))
     except (urllib.error.URLError,TimeoutError):raise SystemExit('Network error; response and billing state unknown; investigate before resuming')
    if a.provider=='meta':
     ch=response['choices'][0];text=ch['message'].get('content') or '';status='completed' if ch.get('finish_reason')=='stop' else 'incomplete';usage=response.get('usage') or {};it=usage.get('prompt_tokens',0);ot=usage.get('completion_tokens',0);cached=usage.get('prompt_tokens_details',{}).get('cached_tokens',0)
    else:
     text=''.join(c.get('text','') for x in response.get('output',[]) if x.get('type')=='message' for c in x.get('content',[]) if c.get('type')=='output_text');status=response.get('status');usage=response.get('usage') or {};it=usage.get('input_tokens',0);ot=usage.get('output_tokens',0);cached=usage.get('input_tokens_details',{}).get('cached_tokens',0)
    cost=None if prices[0] is None else ((it-cached)*prices[0]+ot*prices[1]+cached*prices[2])/1e6
    record={'model':a.model,'trial':n,'task':t['id'],'utc':datetime.now(timezone.utc).isoformat(),'request':payload,'response':response,'status':status,'runtime_seconds':time.monotonic()-start,'input_tokens':it,'output_tokens':ot,'estimated_cost_usd':cost,'grade':grade(text,t['reference']) if status=='completed' else None}
    atomic(out,record);records.append(record)
    completed=[r for r in records if r.get('status')=='completed'];summary={'responses':len(records),'completed_trials':len(completed),'passed':sum(r['grade']['passed'] for r in completed),'input_tokens':sum(r.get('input_tokens',0) for r in records),'output_tokens':sum(r.get('output_tokens',0) for r in records),'runtime_seconds':sum(r['runtime_seconds'] for r in records),'estimated_cost_usd':sum(r['estimated_cost_usd'] for r in records) if records and all(r.get('estimated_cost_usd') is not None for r in records) else None}
    atomic(folder/'summary.json',summary);print(t['id'],n,status,record['grade']['passed'] if record['grade'] else 'unscored',flush=True)
 finally:lock.unlink(missing_ok=True)
if __name__=='__main__':main()
