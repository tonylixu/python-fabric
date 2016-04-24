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
