#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. Call the conda run environment process
2. Then run the Python code within this environment
with JSON file as input (contains parameters for
the Python classes and functions) in Input dir
3. Copy/Paste Output from docker context to 
host directory with "time&date" name to 
avoid substitutions
"""

import subprocess
import json
import os
import shutil
import re
import datetime

input_config = "/Input/config.json"

subprocess.call(
        [
                "conda", 
                "run", 
                "-n", 
                "geodecision", 
                "python", 
                "get_graph.py", 
                input_config
                ]
        )

if os.path.isfile(input_config):
    with open(input_config) as f: 
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
else: 
    raise FileNotFoundError(
            "ERROR: Please check if {} exists".format(input_config)
            )
