
import csv
import os
import sys
import requests
from dotenv import load_dotenv

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

    # Test if the token can read the repo first
    test_url = f"https://github.com/{org_name}/{base_repo}"
    test_response = requests.get(test_url, headers=headers)

    if test_response.status_code == 200:
        print("Authentication successful! The repo is visible.")
    elif test_response.status_code == 404:
        print("The repo cannot be found. Check your token permissions or repo spelling.")
    else:
        print(f"Error {test_response.status_code}: {test_response.text}")
    #=== END TEST

    #sys.exit(1)

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:

            if not row or len(row) < 2:
                print(f'Invalid row: {row}')
                continue

            class_id = row[0].strip()
            username = row[1].strip()
            repo_name = f"{class_id}-{username}-work"

            print(f"Processing: {repo_name}...")

            # 1. Create the repository in the organization
            #create_url = f"{base_url}/orgs/{org_name}/repos"
            fork_url = f"{base_url}/repos/{org_name}/{base_repo}/forks"
            payload = {
                "name": repo_name,
                "private": True,  # Set to False if you want public repositories
                "organization": org_name #ADDED BY ME
            }

            create_response = requests.post(fork_url, json=payload, headers=headers)

            # print(f'payload: {payload}')
            # print(f'url: {fork_url}')

            if create_response.status_code == 202:
                print(f"  [SUCCESS] Repository '{repo_name}' created.")

                # 2. Invite the user as a collaborator (push permission = editor)
                invite_url = f"{base_url}/repos/{org_name}/{repo_name}/collaborators/{username}"
                invite_payload = {"permission": "push"}

                invite_response = requests.put(invite_url, json=invite_payload, headers=headers)

                if invite_response.status_code in [201, 204]:
                    print(f"  [SUCCESS] Invited '{username}' to '{repo_name}'.")
                else:
                    print(f"  [ERROR] Failed to invite {username}: {invite_response.json().get('message', 'Unknown error')}")
            elif create_response.status_code == 422:
                print(f"  [SKIP] Repository '{repo_name}' already exists or invalid name.")
            else:
                error_msg = create_response.json().get('message', 'Unknown error')
                print(f"  [ERROR] Failed to create repo: {error_msg}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python setup_repos.py <csv_file> <org_name> <repo_name>")
        print("Note: Set GITHUB_TOKEN environment variable.")
        sys.exit(1)

    csv_path = sys.argv[1]
    organization = sys.argv[2]
    base_repo = sys.argv[3]
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    print('ready to go')
    #sys.exit()
    setup_repositories(csv_path, organization, base_repo, token)
