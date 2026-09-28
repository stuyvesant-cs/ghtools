#!/bin/bash
cp ghtool.py ghtool_project/src/ghtool/cli.py
cp create_assignment.py ghtool_project/src/ghtool/
cp manage_org.py ghtool_project/src/ghtool/
cp manage_teams.py ghtool_project/src/ghtool/
cp manage_repos.py ghtool_project/src/ghtool/

sed -i '' 's/^import manage_org$/from . import manage_org/' ghtool_project/src/ghtool/cli.py
sed -i '' 's/^import manage_teams$/from . import manage_teams/' ghtool_project/src/ghtool/cli.py
sed -i '' 's/^import create_assignment$/from . import create_assignment/' ghtool_project/src/ghtool/cli.py
sed -i '' 's/^import manage_repos$/from . import manage_repos/' ghtool_project/src/ghtool/cli.py
