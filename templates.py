import os, shutil, subprocess, json, sys, re
from pathlib import Path
from utilities import *

GH_CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_key_name':'github.com-academic',
    'default_gh_repo_visibility':'--private',
}

LOCAL_CONFIG = {
    'academic_root':'C:\\Users\\ilisien\\Desktop\\academic',
    'current_semester':'sp26'
}

def get_all_gh_repos():
    repo_list = subprocess.run(['gh','repo','list','--json','name'], capture_output=True, text=True)
    repo_list = [repo['name'] for repo in json.loads(repo_list.stdout)]
    return repo_list

def sequential_numbered_repo_number(prefix):
    repos = get_all_gh_repos()
    repos_w_prefix = [int(repo.split("_")[-1]) for repo in repos if prefix in repo]
    if len(repos_w_prefix) == 0:
        return 1
    else:
        return max(repos_w_prefix) + 1

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

    repo_prefix = course_code.replace("_","") + "_" + assignment_type.replace(" ","_") + "_"

    return course_code, repo_prefix + str(sequential_numbered_repo_number(repo_prefix))

def create_gh_repo(repo_name,visibility=GH_CONFIG['default_gh_repo_visibility']):
    return subprocess.run(['gh','repo','new',repo_name,visibility],check=True)

def setup_template_only_gitignore(repo_path):
    shutil.copytree("templates\\only_gitignore",repo_path)

def setup_template_technical_written_hw(repo_path):
    pass

def setup_template_mla_essay(repo_path):
    pass

TEMPLATE_LIBRARY = {

}

def local_git_repo_and_push(course_code,repo_name,template=setup_template_only_gitignore,semester=LOCAL_CONFIG['current_semester']):
    base_path = Path(LOCAL_CONFIG['academic_root']) / semester / course_code
    if not base_path.exists():
        if yn(f"Base path: '{str(base_path)}' doesn't exist; create it?",False):
            base_path.mkdir(parents=True,exist_ok=True)
        else:
            sys.exit("Base path doesn't exist, was told not to create it.")

    repo_path = base_path / repo_name
    if repo_path.exists():
        sys.exit(f"A repo already exists at: '{str(repo_path)}'! Quit so as to not overwrite.")
    else:
        repo_path.mkdir(parents=True,exist_ok=False)
    
    template(repo_path)

    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)