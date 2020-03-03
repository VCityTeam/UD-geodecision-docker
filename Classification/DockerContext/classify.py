#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@author: thomleysens
"""
Created on Thu Feb 13 15:14:20 2020

@author: thomas
"""

import argparse

text = """
Automatic classification for socio-eco data
"""

from geodecision import ClassificationDataFrames 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description = text)
    parser.add_argument("json_config")
    args = parser.parse_args()
    ClassificationDataFrames(args.json_config)