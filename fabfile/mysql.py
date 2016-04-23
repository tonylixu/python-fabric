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

@task
def grab_innodb_stats():
    """
    Query for the current innodb status and dump it to a file.
    """
    with open('innodb-%s.txt' % env.host, 'a') as f:
        f.write(str(datetime.datetime.today()))
        f.write('\n')
        f.write(execute_command_as_root('SHOW ENGINE INNODB STATUS\G'))
        f.write('\n\n\n')
