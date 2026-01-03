import os, shutil, subprocess
from pathlib import Path

sp26 = {
    "courses":{
        'phys':'phys_212h'
    }
}

def fa25_academic_naming(course_code,assignment_type,semester=sp26):
    '''
    Naming in the format: "abc123_assignment_type_1"
    
    :param course_code: string course code, for example "
    :param assignment_type: Description
    '''

CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_key_name':'github.com-academic',
    'default_gh_repo_visibility':'private',
    'repo_naming_standard':
}

def create_gh_repo()