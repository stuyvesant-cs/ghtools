import csv
import os
import requests
import time

def send_request(request_method, url_string, payload, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    base_url = "https://api.github.com"

    url = f'{base_url}{url_string}'
    response = request_method(url, json=payload, headers=headers)
    return response

def user_operations(args):
    if args.users_command == 'add':
        if args.file:
            #print('file add users')
            modify_users(args.file, args.org, args.token)
        else:
            #print('individual add user')
            add_user_to_team(args.username, args.org, args.team, args.token)
    else:
        if args.file:
            #print('file remove users')
            modify_users(args.file, args.org, args.token, True)
        else:
            #print('individual remove user')
            remove_user_from_team(args.username, args.org, args.team, args.token)

def modify_users(csv_file, org_name, token, remove=False):
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

            if remove:
                remove_user_from_team(username, org_name, team_name, token)
            else:
                add_user_to_team(username, org_name, team_name, token)

def add_user_to_team(username, org_name, team_name, token):
    invite_url = f"/orgs/{org_name}/teams/{team_name}/memberships/{username}"
    payload = {
        'role': 'member'
    }

    response = send_request(requests.put, invite_url, payload, token)
    if response.status_code == 200:
        print(f"✅ [SUCCESS] added {username} to {team_name}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to add {username} {response.status_code} {error_msg}")

def remove_user_from_team(username, org_name, team_name, token):
    invite_url = f"/orgs/{org_name}/teams/{team_name}/memberships/{username}"

    response = send_request(requests.delete, invite_url, None, token)
    if response.status_code == 204:
        print(f"✅ [SUCCESS] removed {username} from {team_name}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to remove {username} {response.status_code} {error_msg}")

def create_team(args):
    org_name = args.org
    team_name = args.team
    token = args.token

    create_url = f"/orgs/{org_name}/teams"
    payload = {
        'name': team_name
    }

    #response = requests.post(create_url, json=payload, headers=headers)
    response = send_request(requests.post, create_url, payload, token)
    if response.status_code == 201:
        print(f"✅ [SUCCESS] {team_name} created.")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to create team: {response.status_code} {error_msg}")

def remove_team(args):
    org_name = args.org
    team_name = args.team
    token = args.token

    remove_url = f'/orgs/{org_name}/teams/{team_name}'
    response = send_request(requests.delete, remove_url, None, token)
    if response.status_code == 204:
        print(f"✅ [SUCCESS] removed {team_name}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to remove {team_name} {response.status_code} {error_msg}")


def repo_operations(args):
    if args.repos_command == 'add':
        if args.file:
            #print('file add users')
            modify_repos(args.file, args.org, args.token)
        else:
            #print('individual add user')
            add_repo_to_team(args.repo, args.org, args.team, args.token)
    else:
        if args.file:
            #print('file remove users')
            modify_repos(args.file, args.org, args.token, True)
        else:
            #print('individual remove user')
            remove_repo_from_team(args.repo, args.org, args.team, args.token)

def modify_repos(csv_file, org_name, token, remove=False):
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

            if remove:
                remove_repo_from_team(repo_name, org_name, team_name, token)
            else:
                add_repo_to_team(repo_name, org_name, team_name,token)

def add_repo_to_team(repo_name, org_name, team_name, token, permission='pull'):
    invite_url = f"/orgs/{org_name}/teams/{team_name}/repos/{org_name}/{repo_name}"
    payload = {
        'permission': permission
    }
    #response = requests.put(invite_url, json=payload, headers=headers)
    response = send_request(requests.put, invite_url, payload, token)
    if response.status_code == 204:
        print(f"✅ [SUCCESS] added {repo_name} to {team_name}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to add {repo_name} {response.status_code} {error_msg}")

def remove_repo_from_team(repo_name, org_name, team_name, token):
    invite_url = f"/orgs/{org_name}/teams/{team_name}/repos/{org_name}/{repo_name}"
    #print(invite_url)
    #response = requests.delete(invite_url, headers=headers)
    response = send_request(requests.delete, invite_url, None, token)
    if response.status_code == 204:
        print(f"✅ [SUCCESS] removed {repo_name} from {team_name}")
    else:
        error_msg = response.json().get('message', 'Unknown error')
        print(f"❌ [ERROR] Failed to remove {repo_name} {response.status_code} {error_msg}")
