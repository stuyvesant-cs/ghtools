import argparse
import manage_teams
import manage_org
import create_assignment
from dotenv import load_dotenv
import os
import sys

def parse_team_user_args(args, parser):
    """
    Normalize the positional arguments for:
        team users add
        team users delete

    -i USERNAME TEAM ORG
    -f FILE ORG
    """
    if args.username is not None:
        if len(args.arguments) != 2:
            parser.error("when using -i/--username, TEAM and ORG are required")

        args.team = args.arguments[0]
        args.org = args.arguments[1]

    elif args.file is not None:
        if len(args.arguments) != 1:
            parser.error("when using -f/--file, only ORG should be provided")

        args.team = None
        args.org = args.arguments[0]

    del args.arguments

def parse_team_repo_args(args, parser):
    """
    Normalize the positional arguments for:
        team repos add
        team repos delete

    -i REPO TEAM ORG
    -f FILE ORG
    """
    if args.repo is not None:
        if len(args.arguments) != 2:
            parser.error("when using -i/--repo, TEAM and ORG are required")

        args.team = args.arguments[0]
        args.org = args.arguments[1]

    elif args.file is not None:
        if len(args.arguments) != 1:
            parser.error("when using -f/--file, only ORG should be provided")

        args.team = None
        args.org = args.arguments[0]

    del args.arguments

#===========================
#  WIP
#===========================
def parse_assignment_args(args, parser):
    """
    Normalize the positional arguments for:
        assignment create

    -i PERIOD USERNAME ORG REPO
    -f FILE ORG REPO
    """
    if args.user is not None:
        if len(args.arguments) != 2:
            parser.error("when using -i/--user, PERIOD USERNAME is required")

        args.period = args.user
        args.user = args.arguments[0]
        args.org = args.arguments[1]

    elif args.file is not None:
        if len(args.arguments) != 1:
            parser.error("when using -f/--file, only FILENAME is required")

        args.org = args.arguments[0]

    del args.arguments


def create_parser():
    parser = argparse.ArgumentParser(
        prog="ghtool",
        description="Tools for managing GitHub organizations and teams.")

    # =========================================================
    # TOP LEVEL
    # =========================================================
    top_subparsers = parser.add_subparsers(
        dest="command",
        required=True)

    # =========================================================
    # ORG
    # =========================================================
    org_parser = top_subparsers.add_parser(
        "org",
        help="Organization operations")

    org_subparsers = org_parser.add_subparsers(
        dest="org_command",
        required=True)

    # ---------------------------------------------------------
    # ORG USERS
    # ---------------------------------------------------------
    org_users_parser = org_subparsers.add_parser(
        "users",
        help="Organization user operations")

    org_users_subparsers = org_users_parser.add_subparsers(
        dest="users_command",
        required=True)

    # ---------------------------------------------------------
    # ORG USERS ADD
    # ---------------------------------------------------------
    org_users_add_parser = org_users_subparsers.add_parser(
        "add",
        help="Add users to an organization")

    org_users_input = (
        org_users_add_parser.add_mutually_exclusive_group(
            required=True))

    org_users_input.add_argument(
        "-i",
        "--username",
        metavar="USERNAME",
        help="Username to add")

    org_users_input.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="File containing usernames")

    org_users_add_parser.add_argument(
        "org",
        metavar="ORG",
        help="GitHub organization")
    org_users_add_parser.set_defaults(func=manage_org.org_operation)

    # =========================================================
    # TEAM
    # =========================================================
    team_parser = top_subparsers.add_parser(
        "team",
        help="Team operations")

    team_subparsers = team_parser.add_subparsers(
        dest="team_command",
        required=True)

    # ---------------------------------------------------------
    # TEAM CREATE - DONE
    # ---------------------------------------------------------
    team_create_parser = team_subparsers.add_parser(
        "create",
        help="Create a team")

    team_create_parser.add_argument(
        "team",
        metavar="TEAM",
        help="Team name")

    team_create_parser.add_argument(
        "org",
        metavar="ORG",
        help="GitHub organization")

    team_create_parser.set_defaults(func=manage_teams.create_team)

    # ---------------------------------------------------------
    # TEAM DELETE - DONE
    # ---------------------------------------------------------
    team_delete_parser = team_subparsers.add_parser(
        "delete",
        help="Delete a team")

    team_delete_parser.add_argument(
        "team",
        metavar="TEAM",
        help="Team name")

    team_delete_parser.add_argument(
        "org",
        metavar="ORG",
        help="GitHub organization")

    team_delete_parser.set_defaults(func=manage_teams.remove_team)

    # ---------------------------------------------------------
    # TEAM USERS
    # ---------------------------------------------------------

    team_users_parser = team_subparsers.add_parser(
        "users",
        help="Team user operations")

    team_users_subparsers = team_users_parser.add_subparsers(
        dest="users_command",
        required=True)

    # ---------------------------------------------------------
    # TEAM USERS ADD
    # ---------------------------------------------------------

    team_users_add_parser = team_users_subparsers.add_parser(
        "add",
        help="Add users to a team")

    team_users_add_input = (
        team_users_add_parser.add_mutually_exclusive_group(
            required=True))

    team_users_add_input.add_argument(
        "-i",
        "--username",
        metavar="USERNAME",
        help="Username to add")

    team_users_add_input.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="File containing team/user information")

    team_users_add_parser.add_argument(
        "arguments",
        nargs="+",
        metavar="ARG",
        help="TEAM ORG when using -i; ORG when using -f")
    team_users_add_parser.set_defaults(func=manage_teams.user_operations)

    # ---------------------------------------------------------
    # TEAM USERS DELETE
    # ---------------------------------------------------------

    team_users_delete_parser = team_users_subparsers.add_parser(
        "delete",
        help="Delete users from a team")

    team_users_delete_input = (
        team_users_delete_parser.add_mutually_exclusive_group(
            required=True))

    team_users_delete_input.add_argument(
        "-i",
        "--username",
        metavar="USERNAME",
        help="Username to delete")

    team_users_delete_input.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="File containing team/user information")

    team_users_delete_parser.add_argument(
        "arguments",
        nargs="+",
        metavar="ARG",
        help="TEAM ORG when using -i; ORG when using -f")
    team_users_delete_parser.set_defaults(func=manage_teams.user_operations)

    # ---------------------------------------------------------
    # TEAM REPOS
    # ---------------------------------------------------------

    team_repos_parser = team_subparsers.add_parser(
        "repos",
        help="Team repo operations")

    team_repos_subparsers = team_repos_parser.add_subparsers(
        dest="repos_command",
        required=True)

    # ---------------------------------------------------------
    # TEAM REPOS ADD
    # ---------------------------------------------------------
    team_repos_add_parser = team_repos_subparsers.add_parser(
        "add",
        help="Add a team to a repo")

    team_repos_add_input = (
        team_repos_add_parser.add_mutually_exclusive_group(
            required=True))

    team_repos_add_input.add_argument(
        "-i",
        "--repo",
        metavar="REPO",
        help="Repo to add")

    team_repos_add_input.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="File containing team/repo information")

    team_repos_add_parser.add_argument(
        "arguments",
        nargs="+",
        metavar="ARG",
        help="TEAM ORG when using -i; ORG when using -f")
    team_repos_add_parser.set_defaults(func=manage_teams.repo_operations)

    # ---------------------------------------------------------
    # TEAM REPOS DELETE
    # ---------------------------------------------------------
    team_repos_delete_parser = team_repos_subparsers.add_parser(
        "delete",
        help="Delete a team to a repo")

    team_repos_delete_input = (
        team_repos_delete_parser.add_mutually_exclusive_group(
            required=True))

    team_repos_delete_input.add_argument(
        "-i",
        "--repo",
        metavar="REPO",
        help="Repo to add")

    team_repos_delete_input.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="File containing team/repo information")

    team_repos_delete_parser.add_argument(
        "arguments",
        nargs="+",
        metavar="ARG",
        help="TEAM ORG when using -i; ORG when using -f")
    team_repos_delete_parser.set_defaults(func=manage_teams.repo_operations)

    # =========================================================
    # ASSIGNMENT
    # =========================================================
    assignment_parser = top_subparsers.add_parser(
        "assignment",
        help="Assignment operations")

    assignment_subparsers = assignment_parser.add_subparsers(
        dest="assignment_command",
        required=True)

    # ---------------------------------------------------------
    # Assignment CREATE
    # ---------------------------------------------------------
    assignment_create_parser = assignment_subparsers.add_parser(
        "create",
        help="Create an assignment")
    assignment_create_input = (
        assignment_create_parser.add_mutually_exclusive_group(
            required=True))

    assignment_create_input.add_argument(
        "-i",
        "--user",
        metavar="user",
        help="Period and Username to add")

    assignment_create_input.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="File containing period/username information")

    assignment_create_parser.add_argument(
        "arguments",
        nargs="+",
        metavar="ARG",
        help="PERIOD USERNAME ORG when using -i; ORG when using -f")

    team_create_parser.add_argument(
        "org",
        metavar="ORG",
        help="GitHub organization")

    assignment_create_parser.add_argument(
        "repo",
        metavar="REPO",
        help="Repository name")

    assignment_create_parser.set_defaults(func=create_assignment.assignment_operation)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # team users add/delete need special handling because
    # their positional arguments depend on whether -i or -f
    # was used.
    if (
        args.command == "team"
        and args.team_command == "users"
        and (args.users_command in ("add", "delete"))):
        parse_team_user_args(args, parser)
    if (
        args.command == "team"
        and args.team_command == "repos"
        and (args.repos_command in ("add", "delete"))):
        parse_team_repo_args(args, parser)
    if (
        args.command == "assignment"
        and args.assignment_command == "create"):
        parse_assignment_args(args, parser)

    #print(args)

    load_dotenv()
    token_name = args.org.replace('-', '_').upper()+"_TOKEN"
    token = os.getenv(token_name)
    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)
    args.token = token

    #print(args)

    args.func(args)

if __name__ == "__main__":
    main()
