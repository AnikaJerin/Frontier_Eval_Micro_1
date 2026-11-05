import json,unittest
from pathlib import Path
from grader import grade
ROOT=Path(__file__).resolve().parent

def main():
 tasks=[json.loads(p.read_text()) for p in sorted((ROOT/'data').glob('*.json'))]
 assert len(tasks)==5 and len({t['id'] for t in tasks})==5
 for t in tasks:assert grade(json.dumps(t['reference']),t['reference'])['passed'],t['id']
 print(f'{len(tasks)} selected tasks, {sum(len(t["reference"]) for t in tasks)} reference fields passed')
if __name__=='__main__':main()
