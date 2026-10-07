import json
import platform
from pathlib import Path
import subprocess
import sys
import time
import numpy
import scipy
import matplotlib
HERE = Path(__file__).resolve().parent
results = []
for name in ['check_finite.py', 'check_gaussian.py', 'check_sign.py', 'make_fig_leakage.py']:
    start = time.monotonic()
    run = subprocess.run([sys.executable, str(HERE / name)], cwd=HERE, capture_output=True, text=True)
    results.append(dict(script=name, returncode=run.returncode, elapsed_seconds=time.monotonic() - start, stdout=run.stdout, stderr=run.stderr))
    print(name, 'PASS' if run.returncode == 0 else 'FAIL', flush=True)
record = dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__, matplotlib=matplotlib.__version__, checks=results)
(HERE / 'validation_results.json').write_text(json.dumps(record, indent=2) + '\n')
if any((item['returncode'] for item in results)):
    raise SystemExit('A check failed; see validation_results.json')
