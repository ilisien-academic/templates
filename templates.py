import os, shutil, subprocess, json
from pathlib import Path
from utilities import *

GH_CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_key_name':'github.com-academic',
    'default_gh_repo_visibility':'private',
}

LOCAL_CONFIG = {
    'academic_root':
}

def fa25_academic_naming(course_code,assignment_type,semester='sp26'):
    '''
    Naming in the format: "abc123_assignment_type_1"
    
    :param course_code: course code with underscore, for example "la_197" or reference to semester config, for example "la"
    :param assignment_type: type of assignment to create; warning generated if not in config
    :param semester: semester string to draw defaults from; current default is spring 2026
    '''
    semester_config = load_semester_config()[semester]
    

BASE_CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_key_name':'github.com-academic',
    'default_gh_repo_visibility':'private',
    'naming_standard': fa25_academic_naming,
}

def create_gh_repo()