import json
import sys
from pathlib import Path
p=Path('.secrets_scan.json')
if not p.exists():
    print('no_scan_file')
    sys.exit(0)
b=p.read_bytes()
# try utf-8 then utf-16
for enc in ('utf-8','utf-16'):
    try:
        s=b.decode(enc)
        break
    except Exception:
        s=None
if s is None:
    print('cannot_decode')
    sys.exit(1)
obj=json.loads(s)
results=obj.get('results',{})
if not results:
    print('no findings')
    sys.exit(0)
count=0
for fname, findings in results.items():
    if findings:
        print(f'File: {fname}')
        for f in findings:
            count+=1
            typ=f.get('type')
            ln=f.get('line_number')
            rule=f.get('rule')
            secret=f.get('secret')
            print(f'  - {typ} (rule={rule}) line={ln} secret_preview={str(secret)[:40]}')
print(f'\nTotal findings: {count}')
