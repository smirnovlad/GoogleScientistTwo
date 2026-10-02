from common import *
from scientisttwo.runtime.backends.claude_cli import ClaudeCLIBackend
from scientisttwo.runtime.backends.base import AgentCall
import pathlib
def go():
    c = AgentCall(agent="a", kind="coding", system="s", user="u", schema={"type": "object"}, model="m", effort=None,
                  tools=(), cwd=None, sandbox=None, timeout_s=60, transcript=None, key="k")
    ClaudeCLIBackend(claude_bin=str(pathlib.Path(__file__).parent / "fake_cli.py")).call(c)
