"""Formal SYNOP v1: identical prompt, three independent attempts per model."""
import hashlib,json,shlex,sys,time,urllib.request,urllib.error
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root));from grader import grade,parse
from run_eval import request_api,output_text,write_json
f=Path(__file__).parent;frozen=json.loads((f/'freeze.json').read_text())
for p,h in frozen['sha256'].items():
 if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h:raise SystemExit('Frozen content changed: '+p)
prompt=(f/'prompt.txt').read_text();ref=json.loads((f/'reference.json').read_text());keys={}
for l in (root/'.env').read_text().splitlines():
 n,sep,v=l.partition('=')
 if sep and n.strip() in ('OPENAI_API_KEY','META_API_KEY'):keys[n.strip()]=shlex.split(v,comments=True)[0]
out=root/'results/synop_real_formal_v1';out.mkdir(parents=True,exist_ok=True)
models=[('gpt-5.4','openai',2.5,15,.25),('gpt-6-astra','openai',10,50,1),('muse-wonder-1.0','meta',4,20,.2)]
for model,provider,pi,po,pc in models:
 for trial in range(1,4):
  path=out/f'{model}_{trial}.json'
  if path.exists():continue
  # Budget includes a conservative reservation for the possible next call.
  records=[json.loads(p.read_text()) for p in out.glob('*_?.json')]
  if sum(r.get('cost_usd',0) for r in records)+.12>1:raise SystemExit('Estimated budget limit reached')
  start=time.monotonic()
  if provider=='openai':
   payload={'model':model,'input':prompt,'max_output_tokens':2048,'store':False};response=request_api(payload,keys['OPENAI_API_KEY']);answer=output_text(response);status=response.get('status');u=response.get('usage') or {};it=u.get('input_tokens',0);ot=u.get('output_tokens',0);cached=u.get('input_tokens_details',{}).get('cached_tokens',0)
  else:
   payload={'model':model,'messages':[{'role':'user','content':prompt}],'max_tokens':2048,'reasoning_effort':'minimal'}
   req=urllib.request.Request('https://api.meta.ai/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+keys['META_API_KEY'],'Content-Type':'application/json'})
   try:
    with urllib.request.urlopen(req,timeout=120) as result:response=json.load(result)
   except urllib.error.HTTPError as e:raise SystemExit('Meta HTTP '+str(e.code))
   choice=response['choices'][0];answer=choice['message'].get('content') or '';status='completed' if choice.get('finish_reason')=='stop' else 'incomplete';u=response.get('usage') or {};it=u.get('prompt_tokens',0);ot=u.get('completion_tokens',0);cached=u.get('prompt_tokens_details',{}).get('cached_tokens',0)
  try:parsed=parse(answer)
  except (ValueError,TypeError,RecursionError):parsed=None
  result={'model':model,'trial':trial,'utc':datetime.now(timezone.utc).isoformat(),'request':payload,'response':response,'status':status,'answer':answer,'parsed_json':parsed,'grade':grade(answer,ref) if status=='completed' else None,'usage':u,'cost_usd':((it-cached)*pi+cached*pc+ot*po)/1e6,'runtime_seconds':time.monotonic()-start}
  write_json(path,result);print(model,trial,status,result['grade']['passed'] if result['grade'] else 'unscored',flush=True)
