
import csv
import os
import sys
import requests
from dotenv import load_dotenv
import time

def add_users(csv_file, org_name, github_token):
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
            user_id = 0

            print(f"Processing: {class_id} {username}...")

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
    if len(sys.argv) < 3:
        print("Usage: python setup_repos.py <csv_file> <org_name>")
        print("Note: Set GITHUB_TOKEN environment variable.")
        sys.exit(1)

    csv_path = sys.argv[1]
    organization = sys.argv[2]
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    print('ready to go')
    #sys.exit()
    add_users(csv_path, organization, token)
