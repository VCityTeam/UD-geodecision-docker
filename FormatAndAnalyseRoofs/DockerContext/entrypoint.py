import subprocess
import json
import os
import shutil

subprocess.call(
        [
                "conda", 
                "run", 
                "-n", 
                "geodecision", 
                "python", 
                "get_analysed_roofs.py", 
                "/Input/config.json"
                ]
        )

json_config=os.path.join('/Input', 'config.json')
with open(json_config) as f: 
   params = json.load(f)
   output_dir = params["dir"]["output"]
   target_output_dir = os.path.join("/Output", output_dir)
# FIXME: instead of removing the output dir (with the risk of
# losing information coming from the invocation context), check
# for existence and append some integer to the output directory
# name to avoid collision
if os.path.isdir(target_output_dir):
    shutil.rmtree(target_output_dir)
shutil.copytree(output_dir, target_output_dir)
