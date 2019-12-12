#!/usr/bin/python

import json
import os
import numpy as np

SG_JSON_DIR = "/vision2/u/kevintan/graph-rcnn.pytorch/scene_graphs/"

def main(args):
    for filename in os.listdir(SG_JSON_DIR):
        with open(filename, 'r') as f:
            sg = json.load(f)



if __name__ == '__main__':
    args = parser.parse_args()
    main(args)