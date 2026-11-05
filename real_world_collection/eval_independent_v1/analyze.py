import collections,json
from pathlib import Path
p=Path(__file__).resolve().parent/'results';rs=[json.loads(f.read_text()) for f in p.glob('*.json')]; models=collections.defaultdict(list);tasks=collections.defaultdict(list)
for r in rs:models[r['model']].append(r);tasks[r['task']].append(r)
def result(v):
 complete=[x for x in v if x.get('status')=='completed' and x.get('grade')];passed=sum(x['grade']['passed'] for x in complete); fields=collections.Counter()
 for x in complete:fields.update(x['grade']['fields'])
 return {'saved_records':len(v),'completed':len(complete),'unscored':len(v)-len(complete),'passed':passed,'failed':len(complete)-passed,'field_correct':sum(sum(x['grade']['fields'].values()) for x in complete),'field_total':sum(len(x['grade']['fields']) for x in complete),'known_estimated_cost_usd':round(sum(x.get('estimated_cost_usd') or 0 for x in v),6),'unknown_cost_records':sum(x.get('status')=='interrupted_response_unknown' for x in v)}
out={'overall':result(rs),'models':{k:result(v) for k,v in sorted(models.items())},'tasks':{k:{m:result([x for x in v if x['model']==m]) for m in sorted(set(x['model'] for x in v))} for k,v in sorted(tasks.items())},'failures':[{'task':x['task'],'model':x['model'],'trial':x['trial'],'incorrect_fields':[k for k,v in x['grade']['fields'].items() if not v], 'error':x['grade'].get('error')} for x in rs if x.get('grade') and not x['grade']['passed']]}
print(json.dumps(out,indent=2))
