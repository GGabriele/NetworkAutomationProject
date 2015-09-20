# Standard modules.
import sys
import json
import argparse 
from getpass import getpass

# Local modules.
import db
import interfaces
import bgp
import push

def parse_params_to_devices(params):
    """ Parsing data and storing them inside the db. """
    device_ids = []
    for d in params:
        router_id = d
        hostname = params[d]["hostname"]
        vendor = params[d]["vendor"]
        ports = int(params[d]["ports_number"])
        as_number = int(params[d]["as_number"])
        ip = params[d]["ip_address"]
        db.insert_device(
            router_id, hostname, vendor, ports, as_number, ip)
        device_ids.append(router_id)
    return device_ids

def read_file(filename):
    """ this function reads the node file and returns the content in a
    dictionary format.
    Arguments:
        <filename> string: the file name to read.
    Returns:
        <nodes> dictionary: contains the parsed content of <filename>
            example:
            nodes = {
                "1.1.1.1": {"ip_address": "10.1.1.1", "vendor": "Cisco"..},
                "2.2.2.2": {"ip_address": "10.1.1.2", "vendor": "Cisco"..},
            }
    """
    nodes = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                params = {}
                device_param = line.split()
                for d in device_param:
                    device_list = d.split(';')
                    router_id = device_list[0]
                    hostname = device_list[1]
                    params["hostname"] = hostname
                    vendor = device_list[2]
                    params["vendor"] = vendor
                    ports = device_list[3]
                    params["ports_number"] = ports
                    as_number = device_list[4]
                    params["as_number"] = as_number
                    ip_address = device_list[5]
                    params["ip_address"] = ip_address
                    nodes[router_id] = params
    except IOError:
        print "File %s does not exist!" % filename 
    return nodes

def configure():
    """This creates a nice and userfriendly command line."""
    parser = argparse.ArgumentParser(description="welcome to network_automation_project!"
        "This is a fancy tool enabling dynamic definition and configuration your network.")
    parser.add_argument('-u', '--username', dest='username',
            help='username to login to nodes')
    parser.add_argument('-p', '--password', dest='password',
            help='password to login to nodes')
    parser.add_argument('-f', '--filename', dest='filename',
            help='text file containing the node data (expected format...)')
    return parser.parse_args()

def main(args):
    """ main method to run this script, here's where all the magic begins. """
    # Getting the missing parameters, if any.
    if not args.username:
        args.username = raw_input("Please enter username: ")
    if not args.password:
        args.password = getpass("Please enter password: ")
    if not args.filename:
        args.filename = raw_input("Please enter filename: ")
    # Reading file.
    nodes = read_file(args.filename)
    print (json.dumps(nodes, sort_keys=True, indent=2))
    devices = parse_params_to_devices(nodes)
    for device in devices:
    	print "Start configuring the device whose Router_ID is %s" % device
    	interface_commands = interfaces.interface_configuration(device)
        bgp_commands = bgp.bgp_configuration(device)
        commands = interface_commands + bgp_commands
        print json.dumps(commands, indent=2)
        result = push.push_configuration(args.username, args.password, device, commands)
        if result == 1:
            db.configured(device)

if __name__ == "__main__":
    sys.exit(main(configure()))