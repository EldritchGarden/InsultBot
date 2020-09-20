# This script cleans up the working directory to remove any runtime artifacts #

# remove __pycache__ folders
Get-ChildItem -Directory -Include __pycache__ -Recurse -Path ../ | Remove-Item -Recurse

# remove log files
Get-ChildItem -Include *.log -Recurse -Path ../ | Remove-Item
