import json

def load_semester_config():
    with open('semester_config.json','r') as f:
        config = json.load(f)
    return config

def write_semester_config(config):
    with open('semester_config.json', 'w') as f:
        json.dump(config, f, indent=2)

def yn(prompt,d_yes=True):
    '''
    yes or no prompt
    
    :param prompt: input prompt
    :param d_yes: make default yes? (True)
    '''
    y = "Y" if d_yes else "y"
    n = "n" if d_yes else "N"

    response = input(prompt + f" [{y}/{n}]").strip().lower()
    yes = (response in ["y","yes"]) or (d_yes and (response == ""))

    if yes:
        return True
    else:
        no = (response in ["n","no"]) or (not d_yes and (response == ""))
        if no:
            return False
        else: 
            print("Answer not understood.")
            return yn(prompt,d_yes)