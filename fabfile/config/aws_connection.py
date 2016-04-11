"""This script defines and returns all aws connections
"""
from __future__ import print_function
# From system
import time
import boto
from boto.s3.connection import S3Connection
from boto.route53.connection import Route53Connection

class Connections(object):
    """AWS connection class"""
    def __init__( self, aws_id=None, aws_key=None, debug=0):
        if aws_id is None:
            self.aws_access_key = None
            sys.exit("Please provide AWS access key and secret!!")
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

    def get_route53(self):
        """Return AWS route53 connection"""
        if self.r53 is None:
            try:
                self.r53 = boto.route53.connection.Route53Connection(
                    self.aws_access_key,
                    self.aws_secret_access_key,
                    debug=self.debug)
            except boto.exception.NoAuthHandlerFound:
                self.connect_failure()
        return self.r53
