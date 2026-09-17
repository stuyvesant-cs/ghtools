
import csv
import os
import sys
import requests
from dotenv import load_dotenv
import time
import argparse

def add_users(csv_file, org_name, github_token):
    """
    Reads a CSV file and creates GitHub repositories in an organization,
    then invites the specified users as collaborators.
    """
    # headers = {
    #     "Authorization": f"token {github_token}",
    #     "Accept": "application/vnd.github.v3+json",
    #     "X-GitHub-Api-Version": "2026-03-10"
    # }
    # base_url = "https://api.github.com"

    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        return

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:

            if not row or len(row) < 2:
                print(f'Invalid row: {row}')
                continue

            #class_id = row[0].strip()
            username = row[1].strip()
            #user_id = 0

            print(f"Processing: {username}...")

            add_user(username, org_name, github_token)
            # #step 0: get users github ID (a number)
            # lookup_url = f'{base_url}/users/{username}'
            # response = requests.get(lookup_url, headers=headers)
            # if response.status_code == 200:
            #     user_id = response.json()['id']
            #
            # if response.status_code == 404:
            #     print(f"{username}: GitHub user not found")
            #
            # invite_url = f"{base_url}/orgs/{org_name}/invitations"
            # payload = {
            #     'invitee_id': user_id,
            #     "role": "direct_member"
            # }
            #
            # response = requests.post(invite_url, json=payload, headers=headers)
            #
            # if response.status_code == 201:
            #     print(f"\t ✅ [SUCCESS] {username} invited.")
            # else:
            #     error_msg = response.json().get('message', 'Unknown error')
            #     print(f"\t ❌ [ERROR] Failed to add user: {error_msg}\n\t{response.json()}")

def add_user(username, org_name, github_token):

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    base_url = "https://api.github.com"

    user_id = 0
    #step 0: get users github ID (a number)
    lookup_url = f'{base_url}/users/{username}'
    response = requests.get(lookup_url, headers=headers)
    if response.status_code == 200:
        user_id = response.json()['id']

    if response.status_code == 404:
        print(f"{username}: GitHub user not found")

    invite_url = f"{base_url}/orgs/{org_name}/invitations"
    payload = {
        'invitee_id': user_id,
        "role": "direct_member"
    }

    response = requests.post(invite_url, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"\t ✅ [SUCCESS] {username} invited.")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"\t ❌ [ERROR] Failed to add user: {error_msg}\n\t{response.json()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='org_add_users',
                    description='Add users to a GitHub Organization')
    arg_group = parser.add_mutually_exclusive_group()
    arg_group.add_argument('-f', '--file')
    arg_group.add_argument('-i', '--individual')
    parser.add_argument('org_name')

    args = parser.parse_args()
    organization = args.org_name

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
        add_users(csv_path, organization, token)
    elif args.individual:
        username = args.individual
        add_user(username, organization, token)
