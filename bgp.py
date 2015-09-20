import db
import json
from netaddr import *

AS = "router bgp {0}"
ROUTER_ID = "bgp router-id {0}"
NEIGHBOR = "neighbor {0} remote-as {1}"
REDISTRIBUTE = "redistribute connected"

def _cisco_configuration(router_id, as_number, bgp_info):
	""" This function is used to generate Cisco IOS configurations. """
	command_list = []
	bgp_info_neighbor = bgp_info.split(';')
	for neighbor in bgp_info_neighbor:
		if len(neighbor) > 5:
			neighbor_info = neighbor.split(':')
			as_neighbor = neighbor_info[0].replace("(u'", "")
			id_neighbor = neighbor_info[1]
			# Building BGP configuration.
			as_command = AS.format(as_number)
			id_command = ROUTER_ID.format(router_id)
			neighbor_command = NEIGHBOR.format(id_neighbor, as_neighbor)
			command_list.append(as_command)
			command_list.append(id_command)
			command_list.append(neighbor_command)
	command_list.append(REDISTRIBUTE)
	print json.dumps(command_list, indent=2)
	return command_list 

def _juniper_configuration(router_id, as_number, bgp_info):
	pass

def bgp_configuration(router_id):
	""" This function is used to configure BGP inside our devices. """
	hostname, vendor, ports, as_number, ip = db.get_device_by_id(router_id)
	# Let's engage the user.
	bgp_info = ""
	while True:
		choice = raw_input("Do you want to insert a new BGP peer? (Y/N): ")
		if choice.upper() == 'Y':
			while True:
				peer_as = raw_input("Which AS do you want to peer with?: ")
				try:
					if int(peer_as):
						# Everything is fine.
						break
				except:
					print "You typed an invalid amount of ports. Try again."
			while True:
				try:
					neighbor = IPAddress(raw_input("Type the neighbor ID: "))
					bgp_peer = peer_as + ":" + str(neighbor) + ";"
					bgp_info += bgp_peer
					break
				except:
					print "You typed and invalid neighbor ID. Please insert something in the format x.x.x.x"
		elif choice.upper() == 'N':
			break
		else:
			print "You typed something wrong. Please type 'Y' or 'N'!"
	# Populate db.
	db.insert_neighbor(router_id, bgp_info)
	# What vendor is this?
	if vendor == "Cisco":
		bgp_commands = _cisco_configuration(router_id, as_number, bgp_info)
	else:
		bgp_commands = _juniper_configuration(router_id, as_number, bgp_info)
	return bgp_commands