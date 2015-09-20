# NetworkAutomationProject

This is a Network Automation Project I'm working on to make some practice with Python and DB interaction.

# Executing the project
python network_automation_project.py -u username -p password -f filename.txt

filename.txt contains a list of devices that you want to add to your network. The tool will use this file to populate the sqlite
database and to start configure the network. The user will be asked for some parameters like interface's addresses and BGP
facts in order to build the proper configurations and push them to the devices.
