import hashlib,importlib.util,json,unittest
from pathlib import Path
D=Path(__file__).resolve().parents[1];ROOT=D.parent
spec=importlib.util.spec_from_file_location('real_grader',D/'grader.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
tasks=json.loads((D/'tasks.json').read_text())
class TaskTests(unittest.TestCase):
 def test_freeze_and_distinct_source_reports(self):
  f=json.loads((D/'freeze.json').read_text());self.assertEqual(hashlib.sha256((ROOT/'raw/attributed_reports.jsonl').read_bytes()).hexdigest(),f['dataset_sha256'])
  for name,h in f['sha256'].items():self.assertEqual(hashlib.sha256((D/name).read_bytes()).hexdigest(),h)
  self.assertEqual(len(tasks),24);self.assertEqual(len(set(t['record_id'] for t in tasks)),24)
  prior=set()
  for prior_path in (ROOT/'exploratory').glob('E*.json'): prior.update(json.loads(prior_path.read_text())['record_ids'])
  self.assertFalse(set(t['record_id'] for t in tasks) & prior)
  records={r['record_id']:r for r in map(json.loads,(ROOT/'raw/attributed_reports.jsonl').read_text().splitlines())}
  for task in tasks:
   row=records[task['record_id']];self.assertIn(row['raw'],task['model_visible_prompt']);self.assertEqual(row['sha256'],task['report_sha256']);self.assertNotIn(json.dumps(task['reference']),task['model_visible_prompt'])
 def test_reference_and_each_mutation(self):
  for t in tasks:
   r=t['reference']
   with self.subTest(task=t['id']):self.assertTrue(g.grade(json.dumps(r),r)['passed'])
   for key,val in r.items():
    changes=[not val, 1] if type(val) is bool else ([None, val+'wrong'] if type(val) is str else ([0,'null',False] if val is None else [val+1,str(val),True,None]))
    for value in changes:
     with self.subTest(task=t['id'],field=key,value=value):
      answer=dict(r);answer[key]=value;self.assertFalse(g.grade(json.dumps(answer),r)['passed'])
    answer=dict(r);del answer[key];self.assertFalse(g.grade(json.dumps(answer),r)['passed'])
   answer=dict(r);answer['extra']=2;self.assertFalse(g.grade(json.dumps(answer),r)['passed'])
 def test_json_schema_and_tolerance(self):
  ref=tasks[0]['reference']
  for answer in ('{}','[]','bad','{"x":NaN}','{"x":1,"x":1}'):
   self.assertFalse(g.grade(answer,ref)['passed'])
  r={'x':1};self.assertTrue(g.grade('{"x":1.0000005}',r)['passed']);self.assertFalse(g.grade('{"x":1.000002}',r)['passed'])
 def test_independent_hand_values(self):
  lookup={t['id']:t['reference'] for t in tasks}
  self.assertEqual(lookup['RS05']['precipitation_24h_mm'],15/10)
  self.assertEqual(lookup['RM05']['r28_reported_limit_m'],2000)
  self.assertEqual(lookup['RT04']['wind_at_boundary_kt'],7)
  self.assertEqual(lookup['RT06']['tempo_ceiling_ft_agl'],2*100)
  self.assertIsNone(lookup['RT06']['probability_vertical_visibility_ft'])
  self.assertEqual(lookup['RT07']['probability_tempo_visibility_m'],500)
if __name__=='__main__':unittest.main()
