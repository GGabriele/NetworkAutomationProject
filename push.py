import db
import json
import time
from netaddr import *
from netmiko import ConnectHandler

SHOW_RUN = "do show run"

def _cisco_push(user, password, ip, command_list, device_type="cisco_ios"):
	""" This function helps to push configurations inside Cisco IOS devices. """
	device = {
		'device_type': device_type,
		'ip': ip,
		'username': user,
		'password': password,
		'secret': password
	}
	try:
		net_connect = ConnectHandler(**device)
		net_connect.enable()
		net_connect.send_config_set(command_list)
		output = net_connect.send_command_expect(SHOW_RUN)
		print "Configuration pushed!"
		return output
	except:
		print "ERROR! Something wrong happened during the configuration process."
		return 0

def _juniper_push(user, password, ip, command_list, device_type="juniper_junos"):
	pass

def push_configuration(user, password, router_id, command_list):
	""" This function helps to push configurations inside network devices. """
	hostname, vendor, ports, as_number, ip = db.get_device_by_id(router_id)
	# What vendor is this?
	if vendor == "Cisco":
		command_results = _cisco_push(user, password, ip, command_list)
	else:
		command_results = _juniper_push(user, password, ip, command_list)
	if command_results is not 0:
		# Create a file with the configuration output.
		filename = hostname + "_configuration.txt"
		with open(filename, 'a') as f:
			f.write(command_results)
			print "Configuration saved!"
			return 1
	else:
		return 0
