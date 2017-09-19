from __future__ import print_function
from __future__ import absolute_import
'''This python file retrieves the secret that you stored in
a local configruation file. This way you don't need to expose
the important information such as password or api keys in the
program

This script reads ~/.fabric_config file and finds matching values

Example:
$ cat ~/.fabric_config
mysql:
    user: 'root'
    password: 'mysql_root'

Then, if you call the from_secret function:
    from_secret('mysql', 'user') returns 'root'
    from_secret('mysql', 'password') returns 'mysql_root'
'''