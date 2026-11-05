import json,unittest
from pathlib import Path
from grader import grade
ROOT=Path(__file__).resolve().parents[1]
def extract(r):
 if 'answer' in r:return r['answer']
 return ''.join(c.get('text','') for o in r['response'].get('output',[]) if o.get('type')=='message' for c in o.get('content',[]) if c.get('type')=='output_text')
class Results(unittest.TestCase):
 def test_all_saved_responses_match_frozen_prompts_and_grades(self):
  tasks={p.stem:json.loads(p.read_text()) for p in (ROOT/'data').glob('*.json')}
  for task,t in tasks.items():
   for model in ('gpt-5.4','gpt-6-astra','muse-wonder-1.0'):
    for trial in range(1,4):
     with self.subTest(task=task,model=model,trial=trial):
      r=json.loads((ROOT/'results'/f'{model}_{task}_{trial}.json').read_text())
      request=r['request'];prompt=request.get('input') if isinstance(request.get('input'),str) else request['messages'][0]['content']
      self.assertEqual(prompt,t['model_visible_prompt']);self.assertEqual(request['model'],model)
      self.assertEqual(grade(extract(r),t['reference']),r['grade'])
 def test_observed_selection_rule(self):
  for task in (p.stem for p in (ROOT/'data').glob('*.json')):
   def passes(model):return sum(json.loads((ROOT/'results'/f'{model}_{task}_{i}.json').read_text())['grade']['passed'] for i in range(1,4))
   with self.subTest(task=task):
    self.assertLess(passes('gpt-5.4'),3);self.assertEqual(passes('gpt-6-astra'),3);self.assertEqual(passes('muse-wonder-1.0'),3)
