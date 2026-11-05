import io,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import run_eval
class Runner(unittest.TestCase):
 def test_incremental_resume(self):
  response={'status':'completed','model':'mock','usage':{'input_tokens':10,'output_tokens':5},'output':[{'type':'message','content':[{'type':'output_text','text':'{}'}]}]}
  calls=[]
  def fake(req,timeout):calls.append(req);return io.BytesIO(json.dumps(response).encode())
  with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,{'OPENAI_API_KEY':'fake-test-token'}),patch('urllib.request.urlopen',side_effect=fake),patch.object(sys,'argv',['run_eval.py','--model','mock','--trials','1','--output',directory]):
   run_eval.main();self.assertEqual(len(calls),5)
   run_eval.main();self.assertEqual(len(calls),5)
   folder=next(Path(directory).iterdir());summary=json.loads((folder/'summary.json').read_text())
   self.assertEqual(summary['completed_trials'],5);self.assertEqual(summary['passed'],0);self.assertEqual(summary['input_tokens'],50);self.assertIsNone(summary['estimated_cost_usd'])
