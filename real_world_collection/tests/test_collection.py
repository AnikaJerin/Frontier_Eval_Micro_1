import hashlib,importlib.util,json,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1];e=p/'exploratory'
spec=importlib.util.spec_from_file_location('experiment_grader',e/'grader.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class CollectionTests(unittest.TestCase):
 def test_source_and_freeze_hashes(self):
  f=json.loads((e/'freeze.json').read_text());self.assertEqual(hashlib.sha256((p/'raw/attributed_reports.jsonl').read_bytes()).hexdigest(),f['source_sha256'])
  for n,h in f['sha256'].items():self.assertEqual(hashlib.sha256((e/n).read_bytes()).hexdigest(),h)
 def test_references_and_mutations(self):
  for path in sorted(e.glob('E*.json')):
   task=json.loads(path.read_text());ref=task['reference'];self.assertTrue(g.grade(json.dumps(ref),ref)['passed'])
   for k,v in ref.items():
    for value in ([not v, 1] if type(v) is bool else ([v+'wrong',None] if type(v) is str else [v+1,str(v),True,None])):
     with self.subTest(task=task['id'],field=k,value=value):
      answer=dict(ref);answer[k]=value;self.assertFalse(g.grade(json.dumps(answer),ref)['passed'])
    answer=dict(ref);del answer[k];self.assertFalse(g.grade(json.dumps(answer),ref)['passed'])
   answer=dict(ref);answer['extra']=0;self.assertFalse(g.grade(json.dumps(answer),ref)['passed'])
 def test_invalid_json(self):
  r={'claim':False}
  for x in ('','[]','null','{"claim": false, "claim": false}','{"claim":NaN}','{"claim": false} trailing'):
   self.assertFalse(g.grade(x,r)['passed'])
 def test_evidence_contradictions(self):
  for task_id in ('E01','E03'):
   task=json.loads((e/(task_id+'.json')).read_text());ref=task['reference'];answer=dict(ref)
   for k in ref:
    if k.startswith('independent'):
     answer[k]=True;self.assertFalse(g.grade(json.dumps(answer),ref)['passed']);answer[k]=False
 def test_manual_arithmetic(self):
  e2=json.loads((e/'E02.json').read_text())['reference'];e3=json.loads((e/'E03.json').read_text())['reference']
  self.assertEqual((e2['observed_visibility_m'],e2['initial_prevailing_forecast_visibility_m'],e2['tempo_forecast_visibility_m']),(3200,3500,2000))
  self.assertAlmostEqual(222/10-210/10,e3['temperature_dewpoint_spread_c'])
  self.assertEqual((e3['pressure_change_24h_hpa'],e3['precipitation_24h_mm']),(-8/10,20/10))
if __name__=='__main__':unittest.main()
