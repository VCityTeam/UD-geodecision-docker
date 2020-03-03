import subprocess
import json
import os
import shutil
import re
import datetime

input_config = "/Input/config.json"

if os.path.isfile(input_config):
    subprocess.call(
            [
                    "conda", 
                    "run", 
                    "-n", 
                    "geodecision", 
                    "python", 
                    "classify.py", 
                    input_config
                    ]
            )

    with open(input_config) as f: 
       params = json.load(f)
       output_dir = params[0]["output_dir"]
       target_output_dir = os.path.join("/Output", output_dir)
    
    if os.path.isdir(target_output_dir):
        target_output_dir = target_output_dir + "_" + re.sub(
                r"[-: ]", "_", str(
                        datetime.datetime.now()
                ).split(".")[0]
        )
    shutil.copytree(output_dir, target_output_dir)
else: 
    raise FileNotFoundError(
            "ERROR: Please check if {} exists".format(input_config)
            )