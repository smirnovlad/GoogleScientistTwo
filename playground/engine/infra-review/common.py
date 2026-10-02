import sys, shutil, pathlib
WT = "<engine>"
sys.path.insert(0, WT); sys.path.insert(0, WT + "/tests")
from conftest import build_toy_task, params  # noqa
from scientisttwo.config import load_profile  # noqa

def fresh_dir(name):
    d = pathlib.Path(__file__).parent / "work" / name
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    return d

def quick(parallel=1, max_wait=0):
    p = load_profile("quick"); p["parallel"] = parallel; p["rate_limit"]["max_wait_minutes"] = max_wait
    return p
