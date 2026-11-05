"""Budget-capped remote inference; local prompts and grading. Never prints keys."""
import argparse,hashlib,importlib.util,json,os,random,shlex,sys,time,urllib.error,urllib.request
from datetime import datetime,timezone
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parent;PROJECT=ROOT.parent
sel=json.loads((D/'selection.json').read_text())
def load_grader():
 spec=importlib.util.spec_from_file_location('real_eval_grader',ROOT/'decoding_v1/grader.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
G=load_grader()
def verify_freeze(folder):
 freeze=json.loads((folder/'freeze.json').read_text())
 for name,h in freeze['sha256'].items():
  if hashlib.sha256((folder/name).read_bytes()).hexdigest()!=h:raise RuntimeError('Frozen input changed: '+name)
verify_freeze(ROOT/'decoding_v1');verify_freeze(ROOT/'exploratory')
all_dec={t['id']:t for t in json.loads((ROOT/'decoding_v1/tasks.json').read_text())}
tasks=[]
for task_id in sel['decoding_task_ids']:tasks.append(all_dec[task_id])
for task_id in sel['exploratory_task_ids']:
 t=json.loads((ROOT/'exploratory'/f'{task_id}.json').read_text());tasks.append({'id':t['id'],'model_visible_prompt':t['prompt'],'reference':t['reference']})
config={'selection_sha256':hashlib.sha256((D/'selection.json').read_bytes()).hexdigest(),'decoding_freeze_sha256':hashlib.sha256((ROOT/'decoding_v1/freeze.json').read_bytes()).hexdigest(),'exploratory_freeze_sha256':hashlib.sha256((ROOT/'exploratory/freeze.json').read_bytes()).hexdigest(),'model_settings':{'gpt-5.4':{'provider':'openai','max_output_tokens':2048},'gpt-6-astra':{'provider':'openai','max_output_tokens':2048},'muse-wonder-1.0':{'provider':'meta','max_output_tokens':2048,'reasoning_effort':'minimal'}},'trials':3,'pricing_note':'Prior run assumed per million USD; estimates only, actual billing may differ','rates_usd_per_million':{'gpt-5.4':[2.5,15,.25],'gpt-6-astra':[10,50,1],'muse-wonder-1.0':[4,20,.2]}}
def write(path,obj):
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n');tmp.replace(path)
config_path=D/'config.json'
if config_path.exists() and json.loads(config_path.read_text())!=config:raise SystemExit('Run config changed; use a separately versioned experiment')
write(config_path,config)
def load_keys():
 result={k:os.environ.get(k) for k in ('OPENAI_API_KEY','META_API_KEY')}
 env_path=PROJECT/'.env'
 for line in (env_path.read_text().splitlines() if env_path.exists() else []):
  name,sep,val=line.partition('=');name=name.strip()
  if sep and name in result and not result[name]:
   parsed=shlex.split(val,comments=True)
   if parsed:result[name]=parsed[0]
 if not all(result.values()):raise SystemExit('Required API key missing; no calls made')
 return result

def extract(response,provider):
 if provider=='meta':
  choice=response['choices'][0];text=choice['message'].get('content') or '';status='completed' if choice.get('finish_reason')=='stop' else 'incomplete';u=response.get('usage') or {};return text,status,u,u.get('prompt_tokens',0),u.get('completion_tokens',0),u.get('prompt_tokens_details',{}).get('cached_tokens',0)
 text=''.join(c.get('text','') for x in response.get('output',[]) if x.get('type')=='message' for c in x.get('content',[]) if c.get('type')=='output_text');u=response.get('usage') or {};return text,response.get('status'),u,u.get('input_tokens',0),u.get('output_tokens',0),u.get('input_tokens_details',{}).get('cached_tokens',0)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=D/'results');parser.add_argument('--decoding-only',action='store_true');args=parser.parse_args()
 keys=load_keys();out=args.output;out.mkdir(parents=True,exist_ok=True)
 for task in tasks:
  if args.decoding_only and task['id'].startswith('E'):continue
  for model,settings in config['model_settings'].items():
   for n in range(1,4):
    path=out/f"{task['id']}_{model}_{n}.json"
    if path.exists():continue
    existing=[json.loads(p.read_text()) for p in out.glob('*.json')]
    if sum(r.get('estimated_cost_usd',0) for r in existing)+.12>sel['approximate_estimated_cost_cap_usd']:raise SystemExit('Stopped at conservative estimated budget reservation; prior results preserved')
    provider=settings['provider'];prompt=task['model_visible_prompt']
    if provider=='openai':url='https://api.openai.com/v1/responses';payload={'model':model,'input':prompt,'max_output_tokens':2048,'store':False};key=keys['OPENAI_API_KEY']
    else:url='https://api.meta.ai/v1/chat/completions';payload={'model':model,'messages':[{'role':'user','content':prompt}],'reasoning_effort':'minimal','max_tokens':2048};key=keys['META_API_KEY']
    start=time.monotonic()
    for attempt in range(5):
     req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
     try:
      with urllib.request.urlopen(req,timeout=120) as result:response=json.load(result)
      break
     except urllib.error.HTTPError as e:
      if e.code not in (429,500,502,503,504) or attempt==4:raise SystemExit('API HTTP '+str(e.code)+'; results saved')
      retry=e.headers.get('Retry-After','') if e.headers else '';delay=min(45,float(retry)) if retry.replace('.','',1).isdigit() else min(30,2**attempt+random.random());time.sleep(delay)
     except (urllib.error.URLError,TimeoutError):raise SystemExit('Network or timeout: completion and billing state unknown. Inspect before resuming.')
    text,status,usage,it,ot,cached=extract(response,provider);pi,po,pc=config['rates_usd_per_million'][model];cost=((it-cached)*pi+ot*po+cached*pc)/1_000_000
    try:parsed=G.parse(text)
    except (ValueError,TypeError,RecursionError):parsed=None
    record={'task':task['id'],'model':model,'trial':n,'utc':datetime.now(timezone.utc).isoformat(),'request':payload,'response':response,'answer':text,'parsed_json':parsed,'status':status,'grade':G.grade(text,task['reference']) if status=='completed' else None,'usage':usage,'estimated_cost_usd':cost,'runtime_seconds':time.monotonic()-start}
    write(path,record);print(task['id'],model,n,status,record['grade']['passed'] if record['grade'] else 'unscored',flush=True)
if __name__=='__main__':main()
