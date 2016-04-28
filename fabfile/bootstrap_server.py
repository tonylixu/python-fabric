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
