#!/usr/bin/env python3
# build_mapping.py
#  - Silas Cutler
# 
# Generates actor mappings
# python build_mapping.py  >> mapping.json
# mv mapping.json ../
#
import sys
import json
from os import walk


def get_mitre_url(o):
    for ref in o.get('external_references', []):
        if "mitre-attack" == ref.get("source_name", ""):
            return ref.get("url", "")



def main():
    mapping = []
    filenames = next(walk("cti/enterprise-attack/intrusion-set/"), (None, None, []))[2]
    for x in filenames:
        mapping.append(parse_file(x))

    print(json.dumps(mapping))


def parse_file(fname):
    indata = json.loads(open("cti/enterprise-attack/intrusion-set/{}".format(fname), 'r').read())

    for o in indata['objects']:

        name = o.get('name', None)
        if name == None:
            continue
        aliases = o.get('aliases', [name])
        mitre_url = get_mitre_url(o)
        description = o.get('description', "[No description]")

        return {
            "name": name,
            "aliases": aliases,
            "url": mitre_url,
            "description": description 
        }


if __name__ == "__main__":
    main()