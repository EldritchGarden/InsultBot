#!/bin/bash
# Install the venv, necessary packages, and service file

# get paths
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
PACK_ROOT=`dirname $SCRIPTPATH`
cd $PACK_ROOT  # set cwd to package root

# install venv
python3 -m venv venv
venv/bin/python3 -m pip install -r requirements.txt  # install required packages

# install service
PY_PATH="$PACK_ROOT/venv/bin/python3"
MAIN_PATH="$PACK_ROOT/src/main.py"

(  # write service file
cat <<EOF
[Unit]
Description=Insult Bot Runtime Service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=$USER
WorkingDirectory=$PACK_ROOT
ExecStart=$PY_PATH $MAIN_PATH

[Install]
WantedBy=multi-user.target
EOF
) > insult.service

cp insult.service /etc/systemd/system/
systemctl daemon-reload
service insult enable

echo "venv and service installed. Run sudo service insult start"

# do not track changes to config.json or credentials.json
echo "configuring git to ignore config changes..."
git update-index --skip-worktree "$PACK_ROOT/src/config.json"
git update-index --skip-worktree "$PACK_ROOT/src/Update/credentials.json"
