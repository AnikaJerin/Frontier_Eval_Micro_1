"""Audit the separately frozen, user-permitted real SYNOP experiment."""
import hashlib, json, unittest
from pathlib import Path
from grader import grade
ROOT=Path(__file__).resolve().parents[1]
FORMAL=ROOT/'real_synop_case/formal_v1'
class TestRealSynop(unittest.TestCase):
 def test_frozen_hashes_and_reference(self):
  frozen=json.loads((FORMAL/'freeze.json').read_text())
  for name,expected in frozen['sha256'].items():
   with self.subTest(file=name): self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),expected)
  reference=json.loads((FORMAL/'reference.json').read_text())
  self.assertEqual(len(reference),27)
  self.assertTrue(grade(json.dumps(reference),reference)['passed'])
 def test_records_regrade(self):
  ref=json.loads((FORMAL/'reference.json').read_text())
  prompt=(FORMAL/'prompt.txt').read_text()
  records=sorted((ROOT/'results/synop_real_formal_v1').glob('*_?.json'))
  self.assertEqual(len(records),9)
  outcomes={}
  for path in records:
   record=json.loads(path.read_text())
   original=record['request']
   actual=original.get('input') or original['messages'][0]['content']
   self.assertEqual(actual,prompt)
   self.assertEqual(grade(record['answer'],ref),record['grade'])
   outcomes.setdefault(record['model'],[]).append(record['grade']['passed'])
  self.assertEqual({k:sum(v) for k,v in outcomes.items()},{'gpt-5.4':0,'gpt-6-astra':3,'muse-wonder-1.0':2})
 def test_field_mutations(self):
  ref=json.loads((FORMAL/'reference.json').read_text())
  for k,v in ref.items():
   for value in (0 if v is None else v+1,True,str(v)):
    altered=dict(ref);altered[k]=value
    with self.subTest(field=k,value=value):self.assertFalse(grade(json.dumps(altered),ref)['passed'])
   altered=dict(ref);del altered[k]
   self.assertFalse(grade(json.dumps(altered),ref)['passed'])
