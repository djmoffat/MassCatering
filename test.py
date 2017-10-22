#!/usr/bin/env python

import yaml

with open("recipe/dumplings.yaml", 'r') as stream:
    try:
        menu = yaml.load(stream)
        print(menu)
    except yaml.YAMLError as exc:
        print(exc)
