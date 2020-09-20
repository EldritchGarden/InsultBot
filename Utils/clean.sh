# This script cleans up the working directory to remove any runtime artifacts #
# Relative pathing may present issues from outside this Utils dir
# remove __pycache__ folders
rm -rf `find ../ -type d -name __pycache__`

# remove log files
rm -f `find ../ -name *.log`
