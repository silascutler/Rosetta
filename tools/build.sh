git clone https://github.com/mitre/cti.git
cd ./cti/enterprise-attack/intrusion-set
cat * | jq '[ .objects[].name, .objects[].aliases, .objects[].external_references[0].url ]'