import json,unittest
from pathlib import Path
from grader import grade
from validate_submission import main
ROOT=Path(__file__).resolve().parents[1]
class TestGrader(unittest.TestCase):
 def test_validation(self):main()
 def test_references_and_mutations(self):
  for path in (ROOT/'data').glob('*.json'):
   task=json.loads(path.read_text());r=task['reference']
   with self.subTest(task=task['id']):
    self.assertTrue(grade(json.dumps(r),r)['passed'])
    for k,v in r.items():
     wrong=dict(r);wrong[k]=0 if v is None else v+1
     self.assertFalse(grade(json.dumps(wrong),r)['passed'],k)
     wrong=dict(r);del wrong[k];self.assertFalse(grade(json.dumps(wrong),r)['passed'],k)
     wrong=dict(r);wrong[k]=True;self.assertFalse(grade(json.dumps(wrong),r)['passed'],k)
     wrong=dict(r);wrong[k]=str(v);self.assertFalse(grade(json.dumps(wrong),r)['passed'],k)
    wrong=dict(r);wrong['extra']=1;self.assertFalse(grade(json.dumps(wrong),r)['passed'])
 def test_schema(self):
  for text in ('{}','[]','bad','{"x":NaN}','{"x":1,"x":1}'):
   self.assertFalse(grade(text,{'x':1})['passed'])
