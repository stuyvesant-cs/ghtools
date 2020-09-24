from github import Github
import getpass

def login():
    name = input('gh username: ')
    passw = getpass.getpass()
    g = Github(name, passw)
    return g

def get_user_list(fname):
    f = open(fname)
    names = f.read().strip().split()
    f.close()
    return names

def add_user(g, team, user):
    try:
        gh_user = g.get_user(user)
        team.add_membership(gh_user, 'member')
    except:
        print('user ', user, ' not found')

def add_users(g, team, user):
    for user in users:
        print('adding ', user)
        add_user(g, team, user)


if __name__ == '__main__':
    g = login()
    org_name = input('gh org: ')

    try:
        org = g.get_organization( org_name )
    except:
        print('org ', org, ' not found.')

    team_name = input('Team name: ')

    choice = input('create team?[y/N] ')
    if choice == 'y' or choice == 'Y':
        org.create_team( team_name )
        print('Team ', team_name, ' created.')

    #get team
    try:
        team = org.get_team_by_slug(team_name)
    except:
        print('team ', team_name, ' not found')

    choice = input('add single user to team?[y/N] ')
    if choice == 'y' or choice == 'Y':
        user = input('username: ')
        add_user(g, team, user)

    choice = input('batch add users?[y/N] ')
    if choice == 'y' or choice == 'Y':
        fname = input('filename: ')
        users = get_user_list(fname)
        add_users( g, team, users )
