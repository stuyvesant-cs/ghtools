import csv
import os
import sys
import requests
from dotenv import load_dotenv
import time
import argparse

def org_operation(args):
    #print(args)
    if args.org_command == 'users' and args.users_command == 'add':
        if args.file:
            add_users(args.file, args.org, args.token)
        else:
            add_user(args.username, args.org, args.token)

def add_users(csv_file, org_name, github_token):

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
