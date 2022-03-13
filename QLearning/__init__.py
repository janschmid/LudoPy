import os
import os.path as p

script_dir = p.dirname(p.realpath(__file__))
os.makedirs(p.join(script_dir, "Savegames"), exist_ok=True)
os.makedirs(p.join(script_dir, "TestResults"), exist_ok=True)
