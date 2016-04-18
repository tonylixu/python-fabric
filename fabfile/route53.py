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
def list_type_A_records(aws_id, aws_key, domain, boto_debug=False):
    """List all type A records for a given domain"""
    if isinstance(boto_debug, basestring):
        boto_debug = bool(strtobool(boto_debug))
    boto_debug = 2 if boto_debug else 0
    route53_utils = Route53Utils(aws_id, aws_key, debug=boto_debug)

    route53_utils.list_type_A_domain(domain)
