import os, shutil, subprocess
from pathlib import Path

CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_key_name':'github.com-academic',
    'default_gh_repo_visibility':'private',
}

def create_gh_repo()