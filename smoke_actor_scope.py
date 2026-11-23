#!/usr/bin/env python3
"""Regression test for the actor scope ReferenceError in the renderer."""
from pathlib import Path
src=(Path(__file__).resolve().parent/'game.js').read_text()
assert "spawnActor=null" in src
assert "spawnActor=actor;playerMesh=spawnActor(" in src
assert "if(!o&&near&&spawnActor){o=spawnActor(" in src
assert "o=actor(0xa34e46)" not in src
print("Actor scope regression check passed")
