"""This script contains all AWS route53 operations
"""
# For python3 compatabile
from __future__  import (absolute_import, print_function)

from fabric.api import (sudo, task, env)
import pipes
import datetime


def execute_command_as_root(command):
    """Execute a MySQL command as root user"""
    # Be VERY VERY careful with this!!!
    # Assume you have a .my.cnf file in your /root directory
    # [client]
    # user=root
    # password="XXXXXX"
    return sudo('echo %s | mysql --defaults-extra-file=/root/.my.cnf' % pipes.quote(command))

@task
def show_databases():
    """Show all databases"""
    execute_command_as_root('SHOW DATABASES;')