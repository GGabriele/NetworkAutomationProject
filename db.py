import sqlite3 
import os

DB_FILE = 'db.sqlite'
DEVICES_SCHEMA = ('''
    CREATE TABLE devices (
        router_id       TEXT PRIMARY KEY,
        hostname        TEXT,
        vendor          TEXT,
        ports           INT,
        as_number       INT,
        ip_address     TEXT,
        configured      DEFAULT 0)
''')
NEIGHBORS_SCHEMA = ('''
    CREATE TABLE neighbors (
        router_id       TEXT PRIMARY KEY,
        neighbors_list  TEXT)
''')
INTERFACES_SCHEMA = ('''
    CREATE TABLE interfaces (
        router_id       TEXT PRIMARY KEY,
        interface       TEXT)
''')

def _create_schema_if_not_exists(db_file=DB_FILE, devices_schema=DEVICES_SCHEMA, neighbors_schema=NEIGHBORS_SCHEMA, interfaces_schema=INTERFACES_SCHEMA):
    """ Creates a SQLite dataase file if it does not already exist. """
    if not os.path.exists(db_file):
        print "BUILDING DB"
        with sqlite3.connect(db_file) as session:
            session.execute(devices_schema)
            session.execute(neighbors_schema)
            session.execute(interfaces_schema)

def _open_session(db_file=DB_FILE):
    """ Opens a connection to the DB file.
        @return cursor      a database cursor
    """
    return sqlite3.connect(db_file)

def _insert_device(router_id, hostname, vendor, ports, as_number, ip):
    """ Creates a new device based on the parameters provided. """
    session = _open_session()
    sql = ('''
        INSERT INTO devices (router_id, hostname, vendor, ports, as_number, ip_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''')
    cursor = session.cursor()
    cursor.execute(
        sql, (router_id, hostname, vendor, ports, as_number, ip))
    device_id = cursor.lastrowid
    """cursor.execute('SELECT * FROM devices')
    cur = cursor.fetchall()
    for i in cur:
        print i"""
    session.commit()
    session.close()
    return device_id

def insert_device(router_id, hostname, vendor, ports, as_number, ip):
    """ Creates a new device based on the parameters provided. """
    session = _open_session()
    sql = ('''
        SELECT router_id
        FROM devices
        WHERE hostname=? AND vendor=? AND ports=? AND as_number=? AND ip_address=?
    ''')
    result = session.execute(
        sql, (hostname, vendor, ports, as_number, ip)).fetchone()
    if result:
        device_id = result[0]
        return device_id
    return _insert_device(router_id, hostname, vendor, ports, as_number, ip)

def get_device_by_id(router_id):
    """ Gets a device by its unique router_id. """
    session = _open_session()
    sql = ('''
        SELECT hostname, vendor, ports, as_number, ip_address
        FROM devices
        WHERE router_id=?
    ''')
    device = session.execute(sql, (router_id,)).fetchone()
    session.close()
    return device

def get_interfaces_by_id(router_id):
    """ Gets interface info by its unique router_id. """
    session = _open_session()
    sql = ('''
        SELECT interface
        FROM interfaces
        WHERE router_id=?
    ''')
    interface = session.execute(sql, (router_id,)).fetchone()
    session.close()
    return interface

def _insert_interface(router_id, interface_info):
    """ Insert interface information inside the db. """
    session = _open_session()
    sql = ('''
        INSERT INTO interfaces (router_id, interface)
        VALUES (?, ?)
    ''')
    cursor = session.cursor()
    cursor.execute(
        sql, (router_id, interface_info))
    device_id = cursor.lastrowid
    """cursor.execute('SELECT * FROM interfaces')
    cur = cursor.fetchall()
    for i in cur:
        print i"""
    session.commit()
    session.close()

def insert_interface(router_id, interface_info):
    """ Creates a new interface based on the parameters provided. """
    session = _open_session()
    sql = ('''
        SELECT interface
        FROM interfaces
        WHERE router_id=?
    ''')
    result = session.execute(
        sql, (router_id,)).fetchone()
    if result:
        port = result[0]
        return port
    return _insert_interface(router_id, interface_info)

def _insert_neighbor(router_id, bgp_info):
    """ Insert BGP information inside the db. """
    session = _open_session()
    sql = ('''
        INSERT INTO neighbors (router_id, neighbors_list)
        VALUES (?, ?)
    ''')
    cursor = session.cursor()
    cursor.execute(
        sql, (router_id, bgp_info))
    device_id = cursor.lastrowid
    """cursor.execute('SELECT * FROM neighbors')
    cur = cursor.fetchall()
    for i in cur:
        print i"""
    session.commit()
    session.close()

def insert_neighbor(router_id, bgp_info):
    """ Creates a new neighbor based on the parameters provided. """ 
    session = _open_session()
    sql = ('''
        SELECT neighbors_list
        FROM neighbors
        WHERE router_id=?
    ''')
    result = session.execute(
        sql, (router_id,)).fetchone()
    if result:
        if bgp_info in str(result).replace("(u'", ""):
            peer = result[0]
            return peer
    return _insert_neighbor(router_id, bgp_info)

def configured(router_id):
    """ Update the 'configured' value inside the 'devices' table. """
    session = _open_session()
    sql = ('''
        UPDATE devices
        SET configured=1
        WHERE router_id=?
    ''')
    cursor = session.cursor()
    cursor.execute(
        sql, (router_id,)).fetchone()
    device_id = cursor.lastrowid
    session.commit()
    session.close()

_create_schema_if_not_exists()