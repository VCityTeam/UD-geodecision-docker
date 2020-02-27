#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: thomas

import argparse
import os
import json

from geodecision import get_OSM_poly

text = """
Get key/value spatial objects from OSM
"""


def run(json_config):
    """
    Run the methods with the parameters in JSON config file
    """
    #Load params JSON file
    with open(json_config) as f: 
        params = json.load(f)
    
    bbox = params["bbox"]
    key = params["key"]
    value = params["value"]
    driver = params["driver"]
    if driver == "ESRI Shapefile":
        extension = ".shp"
    elif driver == "GeoJSON":
        extension = ".geojson"
    elif driver == "GPKG":
        extension = ".gpkg"
    else:
        raise ValueError(
                """Non avalaible driver. 
                Choose between ESRI Shapefile, GeoJSON or GPKG"""
                )
    output_file = os.path.join(params["output_dir"], (value + extension))
    features = get_OSM_poly(bbox, key, value)
    
    #Check if file exists, delete it if so before writting it 
    #(necessary because of Fiona behavior with GeoJSON)
    try:
        os.remove(output_file)
    except OSError:
        pass
    
    if driver == "GPKG":
        features.to_file(output_file, layer=key+"_"+value, driver=driver)
    else:
        features.to_file(output_file, driver=driver)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description = text)
    parser.add_argument("json_config")
    args = parser.parse_args()
    run(args.json_config)
