import db
import json
from netaddr import *

HOSTNAME = "hostname {0}"
INTERFACE = "interface {0}"
INTERFACE_COMMAND = "ip address {0} {1}"
NO_SHUT = "no shutdown"

def _cisco_configuration(router_id, hostname):
	""" This function is used to generate Cisco IOS configurations. """
	command_list = []
	int_info = db.get_interfaces_by_id(router_id)
	int_info_string =  str(int_info)
	interface_string = int_info_string.split(';')
	for port in interface_string:
		if len(port)>10:
			interface_params = port.split(':')
			int_type = interface_params[0].replace("(u'", "")
			int_addr = interface_params[1] 
			int_mask = interface_params[2]
			# Building interface configuration commands
			hostname_command = HOSTNAME.format(hostname)
			command = INTERFACE.format(int_type)
			interface_command = INTERFACE_COMMAND.format(int_addr, int_mask)
			command_list.append(hostname_command)
			command_list.append(command)
			command_list.append(interface_command)
			command_list.append(NO_SHUT)
	print json.dumps(command_list, indent=2)
	return command_list

def _juniper_configuration(router_id, hostname):
	pass

def interface_configuration(router_id):
	""" This function is used to configure our ports. """
	hostname, vendor, ports, as_number, ip = db.get_device_by_id(router_id)
	# Let's engage the user.
	print "You can configure up to {0} ports.".format(ports)
	while True:
		number = raw_input("How many ports do you want to configure now?:")
		if int(number) > ports:
			print "You typed an invalid amount of ports. Try again."
		else:
			break
	interface_info = ""
	i = 0
	while i < int(number):
		interface_type = raw_input("Interface type and number: (e.g. FastEthernet0/0)")
		while True:
			try:
				interface_addr = IPNetwork(raw_input("IP address (x.x.x.x/x format): "))
				interface = interface_type + ":" + str(interface_addr.ip) + ":" + str(interface_addr.netmask) + ";"
				interface_info += interface
				break
			except:
				print "You typed something wrong! Please insert a valid IP address"
		i += 1
		if i == int(number):
			db.insert_interface(router_id, interface_info)
	# What vendor is this?
	if vendor == "Cisco":
		interface_commands = _cisco_configuration(router_id, hostname)
	else:
		interface_commands = _juniper_configuration(router_id, hostname)
	return interface_commands

