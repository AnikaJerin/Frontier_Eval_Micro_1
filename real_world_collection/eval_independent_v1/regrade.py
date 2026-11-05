"""Recompute saved grades without making any API requests."""
import hashlib,importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parent
spec=importlib.util.spec_from_file_location('grader',R/'decoding_v1/grader.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sel=json.loads((D/'selection.json').read_text()); config=json.loads((D/'config.json').read_text()); assert hashlib.sha256((D/'selection.json').read_bytes()).hexdigest()==config['selection_sha256']
tasks={t['id']:t for t in json.loads((R/'decoding_v1/tasks.json').read_text())}
for tid in sel['exploratory_task_ids']:
 t=json.loads((R/'exploratory'/f'{tid}.json').read_text());tasks[tid]={'model_visible_prompt':t['prompt'],'reference':t['reference']}
count=0
for file in sorted((D/'results').glob('*.json')):
 r=json.loads(file.read_text());t=tasks[r['task']];request=r['request'];prompt=request.get('input') or request['messages'][0]['content'];assert prompt==t['model_visible_prompt'],file
 if r['status']=='completed':assert g.grade(r['answer'],t['reference'])==r['grade'],file;count+=1
 else:assert r['grade'] is None,file
print(f'{count} completed response grades recomputed; saved prompts matched frozen tasks')
