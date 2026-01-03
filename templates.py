import os, shutil, subprocess, json
from pathlib import Path

def fa25_academic_naming(course_code,assignment_type,semester=sp26):
    '''
    Naming in the format: "abc123_assignment_type_1"
    
    :param course_code: course code with underscore, for example "la_197" or reference to semester config, for example "la"
    :param assignment_type: 
    '''

BASE_CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_key_name':'github.com-academic',
    'default_gh_repo_visibility':'private',
    'repo_naming_standard': fa25_academic_naming,
}

def create_gh_repo()