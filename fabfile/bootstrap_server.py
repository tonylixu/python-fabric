"""
This script tries to bootstrap puppet on AWS servers.
"""
# Some good practices
from __future__ import (absolute_import, print_function)
# From system
import re
import string
from os.path import basename
from fabric.api import (abort, hide, prompt, run, settings, sudo, task)
from fabric.contrib.console import confirm
from fabric.contrib.files import (contains, sed, append)
from IPy import IP

# Define own exceptions
class UpdateHostnameError(Exception):
    """Update server hostname exception"""
    pass
class UpdateFileError(Exception):
    """Update file exception"""
    pass
class PackageInstallError(Exception):
    """Install package exception"""
    pass
class SetDefaultError(Exception):
    """Set alternative default exception"""
    pass

@task
def is_installed(package_list):
    """Check if package(s) installed"""
    with settings(
        hide('warnings'),  # stdout will print warnings anyway
        warn_only=True     # Continue execution if puppet not installed
    ):
        result = run("rpm -q {0}".format(package_list))
    return result.succeeded

@task
def update_hostname(hostname):
    """Update hostname (command line and /etc/sysconfig/network)"""
    try:
        with settings(warn_only=True):
            sudo("hostname {0}".format(hostname))   # Run hostname command
            result = run("hostname")
        if result.stdout != hostname:               # If hostname mismatch
            raise UpdateHostnameError
    except UpdateHostnameError:
        abort("Hostname update failed")
    print("Update /etc/sysconfig/network..")
    try:
        with settings(warn_only=True):
            sed('/etc/sysconfig/network',
                before='HOSTNAME=.*',                   # Search string
                after='HOSTNAME={0}'.format(hostname),  # Replace string
                use_sudo=True)
            if not contains(
                    '/etc/sysconfig/network',
                    'HOSTNAME={0}'.format(hostname)):
                raise UpdateFileError
    except UpdateFileError:
        abort("/etc/sysconfig/network update failed")
    print("Hostname updated successfully, hostname: {0}".format(hostname))

@task
def update_hosts_file(master_ip, hostname, alias=None):
    """Update The hosts file to add entry"""
    if not alias:
        alias = hostname.partition('.')[0]
    append('/etc/hosts', "{0} {1} {2}".format(master_ip, hostname, alias), escape=False, use_sudo=True)
