import os, shutil, subprocess, json, sys
from pathlib import Path
from utilities import *

GH_CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_key_name':'github.com-academic',
    'default_gh_repo_visibility':'private',
}

LOCAL_CONFIG = {
    'academic_root':'C:\\Users\\ilisien\\Desktop\\academic',
    'current_semester':'sp26'
}

def fa25_academic_naming(course_code,assignment_type,semester=LOCAL_CONFIG['current_semester']):
    '''
    Naming in the format: "abc123_assignment_type_1"
    
    :param course_code: course code with underscore, for example "la_197" or reference to semester config, for example "la"
    :param assignment_type: type of assignment to create; warning generated if not in config
    :param semester: semester string to draw defaults from; current default is spring 2026
    '''
    SMC_ORIGINAL = load_semester_config()
    semester_config = SMC_ORIGINAL[semester]

    if course_code not in [item for pair in semester_config['courses'].items() for item in pair]:
        if not yn("Could not find chosen course code in config; are you sure this is the right course?",False):
            sys.exit("Exited script, not sure about course code.")
        else:
            if ("_" in course_code) and yn("Add it to semester config?"):
                semester_config["courses"][course_code.split("_")[0]] = course_code
    else:
        if course_code in semester_config['courses']:
            course_code = semester_config['courses'][course_code]
    
    if assignment_type not in semester_config["assignment_types"]:
        if not yn("Could not find chosen assignment type in config; are you sure this is the right type?",False):
            sys.exit("Exited script, not sure about assignment type.")
        else:
            if yn("Add it to semester config?"):
                semester_config["assignment_types"].append(assignment_type)
    



    SMC_ORIGINAL[semester] = semester_config
    write_semester_config(SMC_ORIGINAL)
    

BASE_CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_key_name':'github.com-academic',
    'default_gh_repo_visibility':'private',
    'naming_standard': fa25_academic_naming,
}

def create_gh_repo()