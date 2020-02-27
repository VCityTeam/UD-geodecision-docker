import subprocess
import json
import os
import shutil
import re
import datetime

subprocess.call(
        [
                "conda", 
                "run", 
                "-n", 
                "geodecision", 
                "python", 
                "run.py", 
                "/Input/config.json"
                ]
        )

json_config=os.path.join('/Input', 'config.json')
with open(json_config) as f: 
   params = json.load(f)
   output_dir = params["output_dir"]
   target_output_dir = os.path.join("/Output", output_dir)

if os.path.isdir(target_output_dir):
    target_output_dir = target_output_dir + "_" + re.sub(
            r"[-: ]", "_", str(
                    datetime.datetime.now()
            ).split(".")[0]
    )
shutil.copytree(output_dir, target_output_dir)