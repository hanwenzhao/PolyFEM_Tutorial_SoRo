import os, sys
import json
import numpy as np
import meshplot as mp
import polyfempy as pf

os.chdir(sys.path[0])

json_config = './scene_bowl.json'
with open(json_config, 'r') as f:
    config = json.load(f)

solver = pf.Solver()
solver.set_log_level(1)
solver.set_settings(json.dumps(config))
solver.load_mesh_from_settings()
solver.solve()
