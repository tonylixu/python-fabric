from __future__ import print_function
from __future__ import absolute_import

try:
    import os
    import sys

    # Modules with fabric tasks
    from . import zookeeper
    from . import route53
except ImportError:
    print ("HEY, there was a problem with imports, you might need to run this command:")
    print ("sudo pip install -r fabfile/requirements.txt")
    raise
