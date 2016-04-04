"""Zookeeper fabric utilities"""
from distutils.util import strtobool
from fabric.api import (env, task, warn)
from kazoo.client import (KazooClient, KazooState)
from kazoo.exceptions import NoNodeError

# Default port is 2181, otherwise specify port
# Example: 'zookeeper1.my.com:3333'
zookeeper_hosts = 'zookeeper_host_name'

def my_listener(state):
    if state == KazooState.LOST:
        print("Connection lost!")
    elif state == KazooState.SUSPENDED:
        print("Connection suspended!")
    else:
        print("Connected!")

def __get_zk_connection():
    """Get a zookeeper connection"""
    if not hasattr(__get_zk_connection, 'zk'):
        # Note it is highly recommended that to use a state listener
        # to deal with connection interruptions (TODO)
        __get_zk_connection.zk = KazooClient(hosts=zookeeper_hosts)
        __get_zk_connection.zk.start()

    return __get_zk_connection.zk

@task
def check_znode(path):
    """Create a given znode based on given path"""
    zk = __get_zk_connection()
    zk.add_listener(my_listener)

    # Check if path exists
    if zk.exists(path):
        (data, stat) = zk.get(path)
        print("path: {0} \n" \
            "version: {1} \n" \
            "data: {2}".format(path, stat.version, data.decode("utf-8")))
    zk.stop()

@task
def list_children(path):
    """List the children"""
    zk = __get_zk_connection()
    zk.add_listener(my_listener)

    children = zk.get_children(path)
    print("There are {0} children with names {1}".format(
        len(children), children))
    zk.stop()

@task
def create_path(path):
    """Create a path"""
    zk = __get_zk_connection()
    zk.add_listener(my_listener)

    # Ensure a path, create if necessary
    print("Creating {0}".format(path))
    zk.ensure_path(path)
    zk.stop()

@task
def create_znode(path, data):
    """Create znode with data, data can be null"""
    zk = __get_zk_connection()
    zk.add_listener(my_listener)

    # Create a node with data
    print("Creating znode {0} with value {1}".format(path, data))
    zk.create(path, data)
    zk.stop()

@task
def update_znode(path, data):
    """Update the data for a given znode"""
    zk = __get_zk_connection()
    zk.add_listener(my_listener)

    # Update znode
    print("Updating {0} to {1}".format(path, data))
    zk.set(path, data)
    zk.stop()

@task
def delete_znode(path, recur=True):
    """Remove a path, recursively by default"""
    recur = bool(strtobool(recur)) if isinstance(recur, basestring) else recur

    zk = __get_zk_connection()
    zk.add_listener(my_listener)

    # Delete znode
    print("Deleting {0} recursively({1})".format(path, recur))
    zk.delete(path, recursive=recur)
    zk.stop()
