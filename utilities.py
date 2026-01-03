import json

def load_semester_config():
    with open('semester_config.json','r') as f:
        config = json.load(f)
    return config

def write_semester_config(config):
    with open('semester_config.json', 'w') as f:
        json.dump(config, f, indent=2)