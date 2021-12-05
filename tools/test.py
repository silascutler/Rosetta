#!/usr/bin/env python3
# Author - Silas Cutler
# 
# ref - https://gist.github.com/MSAdministrator/5d152ef57e4021c4ffa242aa02e0fb37

import sys
import requests
from tqdm import tqdm

URL_ENTERPRISEATTACK = 'https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'
URL_OBJPATH = 'https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/{}/{}.json'

REL_MAPPING = {}
ACT_ALTS = {}

def write_output(relationship_list, name):
    fhandle = open(name, 'w')
    fhandle.write(json.dumps(relationship_list))
    fhandle.close()

def fetch(url):
    r = requests.get(url)
    return r.json()

def load_obj_data(o):
    if o in REL_MAPPING:
#        print(o)
        tqdm.write("[CACHED] {}".format(o))

        return REL_MAPPING[o]


    oParams = o.split('--') #[0] == malware// set name | [1] == id val
#    print(oParams)
    nURL = URL_OBJPATH.format(oParams[0], o)
#    print(nURL)
    res = fetch(nURL)
#    print(res.get('objects', {}))
    for sub_o in res.get('objects', []):

        if sub_o.get('type', "") == "intrusion-set":
            #print(sub_o)
            #print(sub_o['name'])

            REL_MAPPING[o] = sub_o['name']
            ACT_ALTS[sub_o['name']] = sub_o.get('aliases', [])
            tqdm.write(sub_o['name'])
            return(sub_o['name'])

#    REL_MAPPING[o] = res
    return None

def main():
    ea = fetch(URL_ENTERPRISEATTACK)
    relationship_list = {}


    for i in tqdm(range(len(ea['objects'])), desc="Loading..."):
        item = ea['objects'][i]
        if 'type' in item:
            if item['type'] == 'relationship':

                source_id = item['source_ref']
                target_id = item['target_ref']

#                if not( source_id.startswith("course-of-action--") or
#                        target_id.startswith("course-of-action--") or
#                        source_id.startswith("attack-pattern--") or
#                        target_id.startswith("attack-pattern--") or
#                        source_id.startswith("tool--") or
#                        target_id.startswith("tool--") 
#                    ):

#                if ((source_id.startswith("malware--") or source_id.startswith("intrusion-set")) and
#                    (target_id.startswith("malware--") or target_id.startswith("intrusion-set"))):
                if (source_id.startswith("intrusion-set--") and source_id.startswith("intrusion-set--")):


                    source_name = load_obj_data(source_id)
                    target_name = load_obj_data(target_id)

                    if source_name is None or target_name is None:
                        continue

                    if source_name not in relationship_list:
                        relationship_list[source_name] = []
                    relationship_list[source_name].append(target_name)

                    if target_name not in relationship_list:
                        relationship_list[target_name] = []
                    relationship_list[target_name].append(source_name)

    write_output(relationship_list, 'mapping.json')
    write_output(ACT_ALTS, 'act.json')

if __name__ == "__main__":
    main()