#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: thomas

import argparse
import json

from geodecision import GetIntersections

text = """
Intersections between potential intersected GPKG file and intersecting GPKG file
"""


def run(json_config):
    """
    Run the methods with the parameters in JSON config file
    """
    #Load params JSON file
    with open(json_config) as f: 
        params = json.load(f)
    
    output = params["output"]
    source_gpkg = params["source_gpkg"]
    intersecting_gpkg = params["intersecting_gpkg"]
    epsg = params["epsg"]
    quadrat_width = params["quadrat_width"]
    driver = params["driver"]

    GetIntersections(
    source_gpkg, 
    intersecting_gpkg, 
    output, 
    epsg=epsg,
    quadrat_width= quadrat_width,
    driver=driver
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description = text)
    parser.add_argument("json_config")
    args = parser.parse_args()
    run(args.json_config)
