"""This script contains all AWS route53 operations
"""
# For python3 compatabile
from __future__  import (absolute_import, print_function)

# From system
import os
import sys
from fabric.api import (abort, task)
from distutils.util import strtobool
# From packages
from .route53_utils import Route53Utils

@task
def check_connection(aws_id, aws_key, boto_debug=False):
    if isinstance(boto_debug, basestring):
        

