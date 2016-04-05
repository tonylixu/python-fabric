"""This script defines and returns all aws connections
"""
from __future__ import print_function
# From system
import time
import boto
from boto.s3.connection import S3Connection
from boto.route53.connection import Route53Connection

# Credentials are expected to be configured in ~/.aws/credentials
# for example:
# [prod]
# aws_access_key_id = XXXXXXXXXXXXXX
# aws_secret_access_key = XXXXXXXXXXXXXX
#
# [test]
# aws_access_key_id = XXXXXXXXXXXXXX
# aws_secret_access_key = XXXXXXXXXXXXXX
class Connections(object):
    """AWS connection class"""
    def __init__(
            self, profile_name='test',
            aws_id=None, aws_key=None, debug=0):
        """Using profile is preferred to explicit access secret keys"""
        if aws_id is None:
            self.profile_name = profile_name
            self.aws_access_key = None
        else:
            self.aws_access_key = aws_id
            self.aws_secret_access_key = aws_key

        self.debug = debug
        if debug > 0:
            boto.set_stream_logger('default.log')
        self.s3 = None
        self.autoscale = None
        self.ec2 = None
        self.cf = None
        self.elb = None
        self.r53 = None

    def connect_failure(self):
        """Handle connection failure"""
        print("Failed to authenticate. " \
               "You will need to create either ~/.boto " \
               "or ~/.aws/credentials")
