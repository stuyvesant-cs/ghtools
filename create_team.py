
import csv
import os
import sys
import requests
from dotenv import load_dotenv
import time
import argparse

def add_users(csv_file, org_name, headers, base_url):
    """
    Reads a CSV file and creates GitHub repositories in an organization,
    then invites the specified users as collaborators.
    """

    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        return

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:

            if not row or len(row) < 2:
                print(f'Invalid row: {row}')
                continue
            username = row[1].strip()
            team_name = row[0].strip()
            print(f"Processing: {username}...")

            add_user_to_team(username, org_name, team_name, headers, base_url)

def add_user_to_team(username, org_name, team_name, headers, base_url):

    invite_url = f"{base_url}/orgs/{org_name}/teams/{team_name}/memberships/{username}"
    payload = {
        'role': 'member'
    }
    #print(invite_url)
    response = requests.put(invite_url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"✅ [SUCCESS] added {username} to {team_name}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to add {username} {response.status_code} {error_msg}")

def create_team(org_name, team_name, headers, base_url):
    create_url = f"{base_url}/orgs/{org_name}/teams"

    payload = {
        'name': team_name
    }

    response = requests.post(create_url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f"✅ [SUCCESS] {team_name} created.")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to create team: {response.status_code} {error_msg}")


def add_repos(csv_file, org_name, headers, base_url):
    """
    Reads a CSV file and creates GitHub repositories in an organization,
    then invites the specified users as collaborators.
    """

    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        return

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:

            if not row or len(row) < 2:
                print(f'Invalid row: {row}')
                continue
            repo_name = row[1].strip()
            team_name = row[0].strip()
            #print(f"Processing: {username}...")

            add_repo_to_team(repo_name, org_name, team_name, headers, base_url)

def add_repo_to_team(repo_name, org_name, team_name, headers, base_url, permission='pull'):
    invite_url = f"{base_url}/orgs/{org_name}/teams/{team_name}/repos/{org_name}/{repo_name}"
    payload = {
        'permission': permission
    }
    #print(invite_url)
    response = requests.put(invite_url, json=payload, headers=headers)
    if response.status_code == 204:
        print(f"✅ [SUCCESS] added {repo_name} to {team_name}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to add {repo_name} {response.status_code} {error_msg}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='org_add_users',
                    description='Add users to a GitHub Organization')
    input_arg_group = parser.add_mutually_exclusive_group()
    action_arg_group = parser.add_mutually_exclusive_group()
    input_arg_group.add_argument('-f', '--file')
    input_arg_group.add_argument('-i', '--individual')

    action_arg_group.add_argument('-r', '--add_repo', action='store_true')
    action_arg_group.add_argument('-t', '--add_team', action='store_true')

    parser.add_argument('-c', '--only_create', action='store_true')
    parser.add_argument('org_name')
    parser.add_argument('team_name')

    args = parser.parse_args()
    organization = args.org_name
    team = args.team_name

    load_dotenv()
    token_name = organization.replace('-', '_').upper()+"_TOKEN"
    token = os.getenv(token_name)

    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    base_url = "https://api.github.com"

    if not (args.only_create or args.add_repo or args.add_team):
        print('please provide -c, -r, or -t option')
        sys.exit(1)
    if args.only_create:
        #print(organization, team, headers, base_url)
        #sys.exit(1)
        create_team(organization, team, headers, base_url)
    if args.add_repo:
        if args.file:
            csv_path = args.file
            add_repos(csv_path, organization, headers, base_url)
        elif args.individual:
            repo = args.individual
            add_repo_to_team(repo, organization, team, headers, base_url)
    elif args.add_team:
        if args.file:
            csv_path = args.file
            add_users(csv_path, organization, headers, base_url)
        elif args.individual:
            username = args.individual
            #create_team(organization, team, headers, base_url)
            add_user_to_team(username, organization, team, headers, base_url)
            #add_user(username, organization, token)
