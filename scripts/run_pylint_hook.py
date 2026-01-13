#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root (adjust if needed)
RCFILE = ROOT / ".pylintrc"
SRC = ROOT / "src"

# collect .py files passed via CLI (e.g., by pre-commit)
files = [f for f in sys.argv[1:] if f.endswith(".py")]

# if nothing was passed, lint the whole src/ tree
targets = files if files else [str(SRC)]

# ensure our project paths are importable
env = os.environ.copy()
env.setdefault("PYTHONPATH", os.pathsep.join([str(ROOT), str(SRC)]))

cmd = [
    sys.executable,
    "-m",
    "pylint",
    "-j",
    "0",
    "--persistent=y",
    "--rcfile",
    str(RCFILE),
    *targets,
]
print("Running:", " ".join(cmd))
result = subprocess.call(cmd, env=env)
sys.exit(result)
