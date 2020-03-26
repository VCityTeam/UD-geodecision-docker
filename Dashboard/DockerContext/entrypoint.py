#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. Call the conda run environment process
2. Then run the Python code within this environment
with JSON file as input (contains parameters for
the Python classes and functions) in Input dir
3. Run bokeh serve to launch the Python Bokeh
webmapping application
"""

import subprocess
import os

input_config = "/Input/bokeh_config.json"

if os.path.isfile(input_config):
    subprocess.call(
            [
                    "conda", 
                    "run", 
                    "-n", 
                    "geodecision",
                    "bokeh",
                    "serve",
                    "dashboard",
                    "--args",
                    input_config
                    ]
            )
else:
    raise FileNotFoundError(
            "ERROR: Please check if {} exists".format(input_config)
            )
