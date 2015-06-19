#!/usr/bin/env python3

import yaml

with open('config.yaml', 'r') as stream:
    print(yaml.load(stream))
