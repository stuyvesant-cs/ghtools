import requests
import subprocess
import os

#only needed for testing
import sys
import argparse
from dotenv import load_dotenv

def send_request(request_method, url_string, payload, params, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    base_url = "https://api.github.com"

    url = f'{base_url}{url_string}'
    response = request_method(url, json=payload, params=params, headers=headers)
    return response

def repo_operations(args):
    repos = get_all_assignment_repos(args.assignment, args.org, args.token)
    if not args.target_dir:
        args.target_dir = './'
    clone_all_assignment_repos(args.assignment, repos, args.user_file, args.make_subdirs, args.target_dir)



def clone_all_assignment_repos(assignment_name, assignment_repos, userfile, make_subdirs=True, base_dir='./'):

    #load usernames and clonenames into a dictionary
    if not os.path.exists(userfile):
        print(f"Error: File '{userfile}' not found.")
        return
    usertext = open(userfile).read().strip().split()
    users = {}
    for user in usertext:
        #print(user)
        ul = user.split(',')
        if len(ul) != 2:
            print(f'\tinvalid row: {user}')
        else:
            users[ul[0]] = ul[1]

    if base_dir[-1] != '/':
        base_dir+= '/'
    base_dir+= f'{assignment_name}'
    if os.path.isdir(base_dir):
        print(f'{base_dir} directory already exists, exiting')
        return
    else:
        os.mkdir(base_dir)

    clone_dir = base_dir
    for repo in assignment_repos:
        if make_subdirs:
            clone_dir = f'{base_dir}/{repo['class_id']}'
            if not os.path.isdir(clone_dir):
                os.mkdir(clone_dir)

        user = repo['username']
        
        if user in users:
            clone_path = f'{clone_dir}/{users[user]}'
            print(f'\ncloning: {repo['ssh_link']}')
            subprocess.run(["git", "clone", repo['ssh_link'], clone_path], check=True)
        else:
            print(f'❌ [ERROR] {user} not in data file')


def clone_assignment(assignment, org_name, userfile, github_token, make_subdirs=True, base_dir='./'):
    repos = get_all_assignment_repos(assignment, org_name, github_token)
    clone_all_assignment_repos(assignment, repos, userfile, make_subdirs, base_dir)

def get_all_assignment_repos(assignment, org_name, github_token):
    repo_names = get_all_repos(org_name, github_token)
    assignment_repos = []
    assignment_name = f'-{assignment}'
    for repo in repo_names:

        if assignment_name in repo:
            ssh_link = repo

            repo = repo[repo.find('/')+1:]
            repo = repo.replace(f'{assignment_name}.git', '')
            class_id = repo[:repo.find('-')]
            username = repo[repo.find('-')+1:]
            assignment_repos.append({
                    'ssh_link' : ssh_link,
                    'class_id' : class_id,
                    'username' : username
            })
    return assignment_repos

def get_all_repos(org_name, github_token, page=1):
    repo_names = []
    while (True):
        #print(f'getting repo page {page}')
        url = f'/orgs/{org_name}/repos'
        payload = {
                'per_page' : 100, #max resposnes per page
                'page' : page}
        response = send_request(requests.get, url, {}, payload, github_token)

        if response.status_code == 200:
            links = response.links
            repos = response.json()
            repo_names+= [r['ssh_url'] for r in repos]
            #print(f'\tlinks: {links}')
            if len(links) == 0 or 'next' not in links:
                return repo_names
            page+= 1
        else:
            error_msg = response.json().get('message', 'Unknown error')
            print(f"❌ [ERROR] Failed to get repositories for: {org_name} {error_msg}\n\t{response.json()}")
            return repo_names

def test_setup(org):
    load_dotenv()
    token_name = org.replace('-', '_').upper()+"_TOKEN"
    token = os.getenv(token_name)
    return token

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('org')

    args = parser.parse_args()
    load_dotenv()
    token_name = args.org.replace('-', '_').upper()+"_TOKEN"
    token = os.getenv(token_name)
    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)
    args.token = token

    get_all_repos(args.org, args.token)
