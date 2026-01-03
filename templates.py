import os, shutil, subprocess, json, sys, re
from pathlib import Path
from utilities import *

GH_CONFIG = {
    'gh_username':'ilisien-academic',
    'gh_email':'irl5102@psu.edu',
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
    subprocess.run(['gh','repo','new',repo_name,visibility],check=True)

def setup_template_only_gitignore(repo_path):
    shutil.copytree("templates\\only_gitignore",repo_path)

def setup_template_technical_written_hw(repo_path):
    JULIA_PACKAGES = ["CairoMakie","DifferentialEquations","Symbolics"]

    shutil.copytree("templates\\technical_written_hw",repo_path)
    subprocess.run(['python','-m','venv','env'],cwd=repo_path / 'code', check=True)
    julia_code = f'using Pkg; Pkg.activate("."); Pkg.add({str(JULIA_PACKAGES).replace("'",'"')})' #; Pkg.precompile()
    subprocess.run(['julia','--project=.','-e',julia_code], cwd=repo_path / 'code', check=True)
    (repo_path / 'REPO_NAME_HERE.tex').rename(repo_path / f'{repo_path.name}.tex')
    long_title = input("What should I title the .tex document? (title): ")
    short_title = input("What is a good short title for this doc? (leave blank for ^): ")
    if short_title == "":
        short_title = long_title
    due_date = input("When is this assignment due? (due date): ")

    

def setup_template_mla_essay(repo_path):
    pass

TEMPLATE_LIBRARY = {
    'empty':setup_template_only_gitignore,
    'tech_informal':setup_template_technical_written_hw,
}

def local_git_repo_and_push(course_code,repo_name,template='empty',semester=LOCAL_CONFIG['current_semester']):
    base_path = Path(LOCAL_CONFIG['academic_root']) / semester / course_code
    if not base_path.exists():
        if yn(f"Base path: '{str(base_path)}' doesn't exist; create it?",False):
            base_path.mkdir(parents=True,exist_ok=True)
        else:
            sys.exit("Base path doesn't exist, was told not to create it.")

    repo_path = base_path / repo_name
    if repo_path.exists():
        sys.exit(f"A repo already exists at: '{str(repo_path)}'! Quit so as to not overwrite.")


    TEMPLATE_LIBRARY[template](repo_path)

    subprocess.run(['git', 'init'], cwd=repo_path, check=True)
    subprocess.run(['git', 'config', 'user.name', GH_CONFIG['gh_username']], cwd=repo_path, check=True)
    subprocess.run(['git', 'config', 'user.email', GH_CONFIG['gh_email']], cwd=repo_path, check=True)
    subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
    subprocess.run(['git', 'commit', '-m', 'init'], cwd=repo_path, check=True)
    
    subprocess.run(['git', 'remote', 'add', 'origin', f'git@{GH_CONFIG["gh_key_name"]}:{GH_CONFIG["gh_username"]}/{repo_name}.git'], cwd=repo_path, check=True)
    subprocess.run(['git', 'branch', '-M', 'main'], cwd=repo_path, check=True)
    subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=repo_path, check=True)

if __name__ == "__main__":
    course_code, repo_name = fa25_academic_naming('math','whw')
    create_gh_repo(repo_name)
    local_git_repo_and_push(course_code, repo_name,template="tech_informal")