
import csv
import os
import sys
import requests
from dotenv import load_dotenv
import time
import argparse

TEMPLATE_SUFFIX = ['-template', '-base']

def assignment_operation(args):
    if args.file:
        setup_repositories(args.file, args.org, args.repo, args.token)
    else:
        create_fork(args.org, args.repo, args.period, args.user, args.token)
        invite_user(args.org, args.repo, args.period, args.user, args.token)

def test_repo_access(org_name, base_repo, github_token):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    # Test if the token can read the repo first
    test_url = f"https://github.com/{org_name}/{base_repo}"
    test_response = requests.get(test_url, headers=headers)

    if test_response.status_code == 200:
        print("Authentication successful! The repo is visible.")
    elif test_response.status_code == 404:
        print("The repo cannot be found. Check your token permissions or repo spelling.")
    else:
        print(f"Error {test_response.status_code}: {test_response.text}")

def setup_repositories(csv_file, org_name, base_repo, github_token):
    """
    Reads a CSV file and creates GitHub repositories in an organization,
    then invites the specified users as collaborators.
    """
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    base_url = "https://api.github.com"

    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        return


    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:

            if not row or len(row) < 2:
                print(f'Invalid row: {row}')
                continue

            class_id = row[0].strip()
            username = row[1].strip()

            print(f"Processing: {username}...")
            fork_success = create_fork(org_name, base_repo, class_id, username, github_token)

            time.sleep(2)

            if  fork_success:
                invite_user(org_name, base_repo, class_id, username, github_token)

def create_fork(org_name, base_repo, class_id, username, github_token):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    base_url = "https://api.github.com"

    repo_name = base_repo
    for suffix in TEMPLATE_SUFFIX:
        if suffix in base_repo:
            repo_name = base_repo.replace(suffix, '')
    repo_name = f"{class_id}-{username}-{repo_name}"

    # 1. Create the repository in the organization
    #create_url = f"{base_url}/orgs/{org_name}/repos"
    fork_url = f"{base_url}/repos/{org_name}/{base_repo}/forks"
    payload = {
        "name": repo_name,
        "private": True,  # Set to False if you want public repositories
        "organization": org_name
    }

    create_response = requests.post(fork_url, json=payload, headers=headers)

    # print(f'payload: {payload}')
    #print(f'url: {fork_url}')

    if create_response.status_code == 202:
        print(f"\t ✅ [SUCCESS] Repository '{repo_name}' created.")
        return True
    elif create_response.status_code == 422:
        print(f"\t ❌ [SKIP] Repository '{repo_name}' already exists or invalid name.")
        return True
    elif create_response.status_code == 403:
        error_msg = create_response.json().get('message', 'Unknown error')
        print(f"\t ❌ [SKIP] Repository '{repo_name}' {create_response.status_code} {error_msg}")
        return True
    else:
        error_msg = create_response.json().get('message', 'Unknown error')
        print(f"\t ❌ [ERROR] Failed to create repo: {create_response.status_code} {error_msg}")
        return False

def invite_user(org_name, base_repo, class_id, username, github_token):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    base_url = "https://api.github.com"

    repo_name = base_repo
    for suffix in TEMPLATE_SUFFIX:
        if suffix in base_repo:
            repo_name = base_repo.replace(suffix, '')
    repo_name = f"{class_id}-{username}-{repo_name}"

    # 2. Invite the user as a collaborator (push permission = editor)
    invite_url = f"{base_url}/repos/{org_name}/{repo_name}/collaborators/{username}"
    invite_payload = {"permission": "push"}

    invite_response = requests.put(invite_url, json=invite_payload, headers=headers)

    if invite_response.status_code in [201, 204]:
        print(f"\t ✅ [SUCCESS] Invited '{username}' to '{repo_name}'.")
    else:
        print(f"\t ❌ [ERROR] Failed to invite {username}: {invite_response.status_code}  {invite_response.json().get('message', 'Unknown error')}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='org_add_users',
                    description='Add users to a GitHub Organization')
    arg_group = parser.add_mutually_exclusive_group()
    arg_group.add_argument('-f', '--file')
    arg_group.add_argument('-i', '--individual', nargs=2)
    parser.add_argument('org_name')
    parser.add_argument('repo_name')

    args = parser.parse_args()

    organization = args.org_name
    base_repo = args.repo_name
    load_dotenv()

    token_name = organization.replace('-', '_').upper()+"_TOKEN"
    token = os.getenv(token_name)

    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    if not (args.file or args.individual):
        print('please provide -f or -i option')
        sys.exit(1)
    elif args.file:
        csv_path = args.file
        setup_repositories(csv_path, organization, base_repo, token)
    elif args.individual:
        username = args.individual[1]
        period = args.individual[0]
        create_fork(organization, base_repo, period, username, token)
        invite_user(organization, base_repo, period, username, token)
        #add_user(username, organization, token)
