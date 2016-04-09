"""This script defines all AWS route53 operation utilities
"""
# For python3 compatabile
from __future__  import (absolute_import, print_function)

# From system
import os
import sys
LIB_PATH = os.path.abspath('fabfile/config')
sys.path.append(LIB_PATH)
from boto.route53.record import ResourceRecordSets
from boto.route53.exception import DNSServerError
# From packages
from aws_connection import Connections
import traceback

aws_id = 'AKIAJPYHAGXD3HOEFXLQ'
aws_key = 'XKeBEmK+IXwzIWewHMeSePR+5eInd8kExmDFpfOO'

class Route53Utils(object):
    """Some standard utilities for working with route53"""
    def __init__(self, aws_id, aws_key debug=0):
        self.connections = Connections(aws_id, aws_key, debug=debug)
        # Change your domain name here!!
        self.env_domain = 'piranhakik.com'

def update_type_A_domain(self, domain, point_to):
    """Update DNS domain record"""
    r53 = self.connection.get_route53()

    # Get Zone ID
    zone = r53.get_zone(self.env.domain)
    zone_id = zone.id

    if not zone.get_a(domain):
        sys.exit("\nAbort: {} does not exists! " \
            "Please create first!".format(domain))

    # Commit change
    try:
        changes = ResourceRecordSets(connection=r53, hosted_zone_id=zone_id)
        change = changes.add_change(action='UPSERT', name=domain, type="A")
        change.set_alias(
            alias_hosted_zone_id=zone_id,
            alias_dns_name=point_to,
            alias_evaluate_target_health=False)
        changes.commit()
    except DNSServerError:
        raise
    except Exception:
        print("Unexpected error: {}".format(traceback.format_exc()))
        sys.exit(1)

    # Print record set
    record = zone.get_a(domain)
    print("\nUpdated record set is:\n{}".format(record.to_print()))
