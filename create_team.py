
import csv
import os
import sys
import requests
from dotenv import load_dotenv
import time
import argparse

# def add_users(csv_file, org_name, github_token):
#     """
#     Reads a CSV file and creates GitHub repositories in an organization,
#     then invites the specified users as collaborators.
#     """
#     # headers = {
#     #     "Authorization": f"token {github_token}",
#     #     "Accept": "application/vnd.github.v3+json",
#     #     "X-GitHub-Api-Version": "2026-03-10"
#     # }
#     # base_url = "https://api.github.com"
#
#     if not os.path.exists(csv_file):
#         print(f"Error: File '{csv_file}' not found.")
#         return
#
#     with open(csv_file, mode='r', encoding='utf-8') as f:
#         reader = csv.reader(f)
#         for row in reader:
#
#             if not row or len(row) < 2:
#                 print(f'Invalid row: {row}')
#                 continue
#
#             #class_id = row[0].strip()
#             username = row[1].strip()
#             #user_id = 0
#
#             print(f"Processing: {username}...")
#
#             add_user(username, org_name, github_token)

def add_user_to_team(username, org_name, team_name, headers, base_url):

    create_url = f"{base_url}/orgs/{org_name}/teams/{team_name}/memberships/{username}"
    payload = {
        'role': 'member'
    }
    print(create_url)
    response = requests.post(create_url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f"\t ✅ [SUCCESS] added {username}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to add {username} {error_msg}\n\t{response.json()}")



def create_team(org_name, team_name, headers, base_url):
    create_url = f"{base_url}/orgs/{org_name}/teams"

    payload = {
        'name': team_name
    }

    response = requests.post(create_url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f" ✅ [SUCCESS] {team_name} created.")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to create team: {error_msg}\n\t{response.json()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='org_add_users',
                    description='Add users to a GitHub Organization')
    arg_group = parser.add_mutually_exclusive_group()
    arg_group.add_argument('-f', '--file')
    arg_group.add_argument('-i', '--individual')
    arg_group.add_argument('-c', '--only_create', action='store_true')
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

    if not (args.file or args.individual or args.only_create):
        print('please provide -c, -f or -i option')
        sys.exit(1)
    elif args.only_create:
        #print(organization, team, headers, base_url)
        #sys.exit(1)
        create_team(organization, team, headers, base_url)
    elif args.file:
        csv_path = args.file
        #add_users(csv_path, organization, token)
    elif args.individual:
        username = args.individual
        create_team(organization, team, headers, base_url)
        add_user_to_team(username, organization, team, headers, base_url)
        #add_user(username, organization, token)
