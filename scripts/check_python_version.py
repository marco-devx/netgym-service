import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        return Path(out)
    except Exception:
        return Path.cwd()


root = repo_root()
pv = root / ".python-version"
tv = root / ".tool-versions"


def read_required() -> str:
    if pv.exists():
        return pv.read_text(encoding="utf-8").strip()
    if tv.exists():
        tokens = tv.read_text(encoding="utf-8").split()
        for t in tokens:
            if t.replace(".", "").isdigit():
                return t
    print("No .python-version/.tool-versions found at", root)
    sys.exit(1)


req = read_required()
parts = [int(x) for x in req.split(".")]
v = sys.version_info
cur = f"{v.major}.{v.minor}.{v.micro}"

same_minor = (v.major, v.minor) == tuple(parts[:2])
same_patch = (len(parts) < 3) or (v.micro == parts[2])

if not (same_minor and same_patch):
    print(f"Python {req} requerido, tienes {cur}")
    sys.exit(1)
