# ghtools
Command line utilities to help replace some of the lost features of GitHub Classroom.


## create_assignment.py
Usage: `python create_assignent.py <csv_file> <org_name> <repo_name>`

Will create repositories forked off an assignment repository and invite students to have write access to the new fork.
- This version assumes that the assignment template and the created student repositories are all in the same organization (`org_name`)
- The `csv_file` assumes each line is the follwoing format: `PERIOD,GH_USERNAME` (e.g. `10,jonalf`). The created repositories will be named `PERIOD-GH_USERNAME`.
- Assumes there is a file `.env` containing the appropriate github access token (see Tokens & Permissions below).

## org_add_users.py
Usage: `python org_add_users.py <csv_file> <org_name>`

Will add all users in `csv_file` to `org_name`. As it stands, it assumes the csv file is the same format as the file for `create_assignment`, notably that means a period column is present on each row, even if the period is not used.


## Tokens & Permissions
### Tokens
In order to use the create_assignment tool, you will need to create a Personal Access Token. GitHub suggests a fine-grained token with the following settings
- Repository Access: All repositories
- Permissions:
  - Repositories:
    - Administartion: Read & Write
    - Contents: Read & Write (Read-only may work here, to be tested)
    - Metatdata: Read-only (this gets turned on automatically)
  - Organizations:
    - Members: Read-only (Read & Write is needed for the org_add_users tool)
  - As written, these programs use python's `dotenv` module to read in tokens from a file called `.env`. They assume the token is stored as `ORG_NAME_TOKEN`. For example:
    - `APCS_DW_TOKEN=alkdjsfniuahf87932hr89jiuihf87y3f43r`
    - The programs will generate the token name based on the `org_name` provided as a command line argument. They will capitalize all letters and replace any `-` characters with `_`.

When making the token, make sure you are in the organization context, as opposed to your personal GitHub account.

### Permissions
There are two places where you need to ensure permissions are correct:
- At the organization level
  - Under Settings --> Member privileges --> Repository Forking
    - Select **User accounts and organizations within this enterprise**
- At the template repository level:
  - Under Settings --> General --> Features
    - Select **Allow forking**
  - If you want the student repositories to be private, the template repository must be private as well.



* * *


some notes from TM:
When I go to 
https://github.com/organizations/fcs251/settings/member_privileges
...and look at the Repository Forking section, there is only this:

[CHECKBOX] Allow forking of private and internal repositories
If enabled, forking is allowed on private, internal, and public repositories. If disabled, forking is only allowed on public repositories. This setting is also configurable per-repository.

...which seems like maybe the same setting, under a different guise?

* * *
Updt 5min later:
Now looking at my template repo ( https://github.com/fcs251/exhaust_tmplt/settings )
...I see the "Allow forking" option is greyed-out. Checkbox uncheckable.

Methinks if I turn on the former, the latter will light up. Investigating...


* * *

2min later:
AHA YES! Checking box for "Allow forking of private and internal repositories" reveals the radiobuttons from which I chose "User accounts and organizations within this enterprise"  -- and when I returned to template repo settings, "Allow forking" is not only no longer greyed out but also ALREADY CHECKED!




PATs at
https://github.com/settings/personal-access-tokens/new


