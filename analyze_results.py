"""Recompute recorded task-level metrics from saved raw responses."""
import json,statistics
from pathlib import Path
from grader import grade
ROOT=Path(__file__).resolve().parent

def get_text(r):
 if 'answer' in r:return r['answer']
 return ''.join(c.get('text','') for o in r['response'].get('output',[]) if o.get('type')=='message' for c in o.get('content',[]) if c.get('type')=='output_text')

def main():
 tasks=[json.loads(p.read_text()) for p in sorted((ROOT/'data').glob('*.json'))];summary={}
 for model in ('gpt-5.4','gpt-6-astra','muse-wonder-1.0'):
  records=[];groups={}
  for task in tasks:
   group=[]
   for n in range(1,4):
    p=ROOT/'results'/f"{model}_{task['id']}_{n}.json";r=json.loads(p.read_text());g=grade(get_text(r),task['reference'])
    if g!=r['grade']:raise ValueError('Saved score mismatch: '+str(p))
    group.append(g['passed']);records.append((r,g))
   groups[task['id']]={'passes':sum(group),'trials':len(group),'pass3':int(all(group))}
  n=len(records);success=sum(g['passed'] for r,g in records)
  cost=sum(r.get('cost_usd',r.get('estimated_cost_usd',0)) or 0 for r,g in records)
  summary[model]={'completed_trials':n,'passes':success,'pass_rate':success/n,'empirical_task_pass3':sum(x['pass3'] for x in groups.values())/len(groups),'mean_task_field_score':statistics.mean(g['score'] for r,g in records),'cost_usd':cost,'runtime_seconds':sum(r['runtime_seconds'] for r,g in records),'per_task':groups}
 print(json.dumps(summary,indent=2));return summary
if __name__=='__main__':main()
