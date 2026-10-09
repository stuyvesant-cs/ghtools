# ghtools
Command line utilities to help replace some of the lost features of GitHub Classroom.

# Now with pip!
The full `ghtool` version of the program is now installable via `pip` from the `ghtool_project` directory.
- To install: run `$ pip install -e .` from `ghtool_project/`
- To run: `$ ghtool`

# CLI Input Schema.
```
ghtool
├── assignment
│   └── create
├── org
│   └── users
│       └── add
├── repo
│   └── clone
└── team
    ├── create
    ├── delete
    ├── repos
    │   ├── add
    │   └── delete
    └── users
        ├── add
        └── delete
```

## ghtool.py
Usage: `python ghtool.py assignment|org|repo|team`
- Assumes there is a file `.env` containing the appropriate GiHub access token (see Tokens & Permissions below).
- All operations are based on working within a single GitHub organization.
- The first thing to do is add all students to the organization (`ghtool org users add`). Students must __accept__ the invitation via GitHub before they can be added to repositories, teams, etc.

### `ghtool.py assignment`
Actions: `create (-i CLASS_ID GH_USERNAME | -f FILE) org_name base_repo`
- Will create repositories based on `base_repo` and invite students to have write access to the new repository.
- If `base_repo` is a Template repository, the new repos will be made from that template.
- If `base_repo` is a regular Repository, the new repos will be _forks_ of `base_repo`. 
- Assumes that the assignment base and the created student repositories are all in the same organization (`org_name`)
- The created repositories will be named `CLASS_ID-GH_USERNAME-ASSIGNMENT` (e.g. `10-jonalf-lab0`).
- `ASSIGNMENT` will be the nave of the `base-repo`. If `base-repo` ends in `-base` or `-template`, those strings will not be included.
- The `csv_file` assumes each line is the following format: `CLASS_ID,GH_USERNAME` (e.g. `10,jonalf`).


### `ghtool repo`
Actions: `clone [-d TARGET_DIR] [-s] ASSIGNMENT ORG USER_FILE`
- Will clone repos if they were made by ghtool.
- `USER_FILE` should be a csv of the form:  `gh_username,dirname`
- The repos will be cloned to `ASSIGNMENT/dirname`.
- `-d` provides an optional directory to store the cloned repos in (default is current directory).
- `-s` Will add the class identifier subdirectory below `ASSIGNMENT/` (`ASSIGNMENT/class_id/dirname`)

### `ghtool.py org`
Actions: `users add (-i USER | -f FILE) org_name`
- If `-f` flag is used, adds all users in `FILE` to `org_name`. As it stands, it assumes the csv file is the same format as the file for assignment creation, that means a `CLASS_ID` column is present on each row, even if that information is not used.
- If `-i` flag is used, will add the GitHub username `USER` to the org.

### `ghtool.py team`
Actions: `team create|delete|repos|users`

#### `create`
Usage: `ghtool.py team create TEAM ORG`
- Add `TEAM` to `ORG`

#### `delete`
Usage: `ghtool.py team delete TEAM ORG`
- Remove `TEAM` from `ORG`

#### `repos`
Usage: `ghtool.py team repos add [-w] (-i REPO TEAM | -f FILE) ORG`
- The options for `add` and `delete` are (almost) the same.
  - `add` will give a team __pull__ access to a repo.
  - `delete` will remove a team as a contributor to a repo.
- If `-i` flag is used, `TEAM` will be added to `REPO`.
- If `-f` flag is used, `FILE` will be parsed, assuming each line is formatted as `TEAM,REPO`. The teams in the file do not need to be the same.
- The `-w` flag only works for the `add` action. If present, it will give __push__ access.
- If a team already has access to a repository, the `add` action can be used to swap between push and pull access.


#### `users`
Usage `ghtool.py team users add (-i USER TEAM | -f FILE) ORG`
- The options for `add` and `delete` are the same.
  - `add` will add a user to a team.
  - `delete` will remove a user from a tram.
- If `-i` flag is used, `USER` will be added to `TEAM`.
- If `-f` flag is used, `FILE` will be parsed, assuming each line is formatted as `TEAM,USER`. The teams in the file do not need to be the same.


## Tokens & Permissions
### Tokens
In order to use this tool, you will need to create a [Personal Access Token](https://github.com/settings/personal-access-tokens/new). GitHub suggests a fine-grained token with the following settings
- Repository Access: All repositories
- Permissions:
  - Repositories:
    - Administartion: Read & Write
    - Contents: Read & Write (Read-only may work here, to be tested)
    - Metatdata: Read-only (this gets turned on automatically)
  - Organizations:
    - Members: Read & Write
  - When making the token, make sure you are in the organization context, as opposed to your personal GitHub account.
- ghtool uses python's `dotenv` module to read in tokens from a file called `.env`. They assume the token is stored as `ORG_NAME_TOKEN`. For example:
  - `APCS_DW_TOKEN=alkdjsfniuahf87932hr89jiuihf87y3f43r`
  - The programs will generate the token name based on the `org_name` provided as a command line argument. They will capitalize all letters and replace any `-` characters with `_`.

### Permissions
There are two places where you need to ensure permissions are correct:
- At the organization level
  - Under Settings --> Member privileges --> Repository Forking
    - Select **User accounts and organizations within this enterprise**
- At the template repository level:
  - Under Settings --> General --> Features
    - Select **Allow forking**
  - If you want the student repositories to be private, the template repository must be private as well.
