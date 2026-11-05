import importlib.util,io,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class RunnerPortability(unittest.TestCase):
 def test_environment_keys_without_env_file(self):
  spec=importlib.util.spec_from_file_location("real_runner",ROOT/"real_world_collection/eval_independent_v1/run.py")
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  with tempfile.TemporaryDirectory() as directory,patch.object(module,"PROJECT",Path(directory)),patch.dict(os.environ,{"OPENAI_API_KEY":"test-openai","META_API_KEY":"test-meta"},clear=True):
   self.assertEqual(module.load_keys(),{"OPENAI_API_KEY":"test-openai","META_API_KEY":"test-meta"})
 def test_fresh_inference_saves_response_without_network(self):
  spec=importlib.util.spec_from_file_location("real_runner_smoke",ROOT/"real_world_collection/eval_independent_v1/run.py")
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  payload={"status":"completed","output":[{"type":"message","content":[{"type":"output_text","text":json.dumps(module.tasks[0]["reference"])}]}],"usage":{"input_tokens":2,"output_tokens":3}}
  with tempfile.TemporaryDirectory() as directory,patch.object(module,"PROJECT",Path(directory)),patch.dict(os.environ,{"OPENAI_API_KEY":"test-openai","META_API_KEY":"test-meta"},clear=True),patch.object(module.sys,"argv",["run.py","--output",str(Path(directory)/"fresh")]),patch.object(module.urllib.request,"urlopen",side_effect=[io.BytesIO(json.dumps(payload).encode()),SystemExit("stop after one")]):
   with self.assertRaises(SystemExit):module.main()
   saved=list((Path(directory)/"fresh").glob("*.json"));self.assertEqual(len(saved),1)
   record=json.loads(saved[0].read_text());self.assertTrue(record["grade"]["passed"]);self.assertNotIn("test-openai",saved[0].read_text())
 def test_output_argument_present(self):
  text=(ROOT/"real_world_collection/eval_independent_v1/run.py").read_text()
  self.assertIn("parser.add_argument('--output'",text)
