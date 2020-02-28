#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@author: thomleysens
"""
Created on Thu Feb 13 15:14:20 2020

@author: thomas
"""
import os
import osmnx as ox
import argparse
import json

from geodecision.graph.utils import graph_to_df, graph_with_time


text = """
Get graph (from OSM network data) with updated edges value
"""

def run(json_config):
    """
    """
    #Load params JSON file
    with open(json_config) as f: 
        params = json.load(f)

    #Get a small bounding box to get network
    ##from Geofabrik Tile Calculator, [left, bottom, right, top]
    bbox = params["bbox"] 
    
    #bbox => north, south, east, west
    graph = ox.graph_from_bbox(
        bbox[3],
        bbox[1],
        bbox[2],
        bbox[0],
        network_type = params["network_type"],
        simplify = params["simplify"]
    )
    
    # Add time as weight in graph (based on walk speed)
    walk_distance = params["walk_distance"] #in meters for 1 hour trip
    graph = graph_with_time(graph, walk_distance)
    
    #Write graph to disk as 2 files (nodes and edges)
    nodes_path = os.path.join(params["output_dir"], params["nodes_name"])
    edges_path = os.path.join(params["output_dir"], params["edges_name"])
    graph_to_df(graph, edges_path, nodes_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description = text)
    parser.add_argument("json_config")
    args = parser.parse_args()
    run(args.json_config)
    