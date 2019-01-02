from __future__ import absolute_import
from __future__ import print_function
# coding: utf8
'''Send message to slack channel through
@notify decorator

https://github.com/kurttheviking/python-simple-hipchat
'''
import slack
import slack.chat
import traceback
from datetime import datetime
from functools import wraps
from fabric.api import task, env, run
from fabric.decorators import _wrap_as_new
from datetime import datetime
import random
from . import credentials


def slack_message(msg):
    '''Send message to #server-notification on slack.

    You should typically use @notify decorator instead of this directly

    Args:
        msg: the message to send
    '''
    try:
        slack.api_token = credentials.get_credentials('slack', 'token')
        slack.chat.post_message('#server-notification', msg, username=credentials.get_credentials('slack', 'user'))
    except:
        print('Problem with slack. Continuing without it. {0}'.format(traceback.format_exc()))


def send_notifications(msg):
    '''Send message to third-party services.

    You should use @notify decorator instead of this directly.

    Args:
       msg: the message to send
    '''
    slack_message(msg)


def easter():
    fun_msg = [ "OMG, Nice code!",
                "On fire!",
                "Godspeed",
                "!!"]
    a = random.randint(0, 3)
    return fun_msg[a]

def notify(func):
    '''Notification decorator.

    To use, simply apply @notify to the fabric task method.
    '''

    # Argument formatting copied from: http://wordaligned.org/articles/echo
    code = func.func_code  # Func's code obj in bytecode
    arg_count = code.co_argcount  # Number of arguments
    arg_names = code.co_varnames[:arg_count]  # Name of each argument
    fn_defaults = func.func_defaults or list()  # Default value of keyword argument
    # Groups default arguments name and its value
    arg_defs = dict(zip(arg_names[-len(fn_defaults):], fn_defaults))

    # The implementation pattern here is based off the @runs_once decorator implementation
    @wraps(func)
    def wrapped(*v, **k):
        # Only send notificationonce per host
        if not hasattr(notify, 'notified_hosts'):
            notify.notified_hosts = set([])  # Define set

        # If env.host is not in notify.notified_hosts, we send notifications
        send_notification = env.host not in notify.notified_hosts
        # Add host into notified_hosts
        notify.notified_hosts.add(env.host)

        if send_notification:
            positional = map(_format_arg_value, zip(arg_names, v))
            defaulted = [_format_arg_value((a, arg_defs[a])) for a in arg_names[len(v):] if a not in k]
            nameless = map(repr, v[arg_count:])
            keyword = map(_format_arg_value, k.items())
            args = positional + defaulted + nameless + keyword

            # The prefix used for notifications:
            easter_msg = easter()
            prefix = '[{}] - {} [{}] {}.{}({})'.format(
                    easter_msg,
                    datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M:%S'),
                    None if env.host is None else env.host.replace('.lixu.ca', ''),
                    func.__module__.replace('fabfile.', ''),
                    func.func_name, ','.join(args)
                )
            send_notifications('{}'.format(prefix))
        try:
            # Now actually invoke it
            return func(*v, **k)
        except BaseException as e:
            if send_notification:
                send_notifications("{}\nFAILED! {} {}".format(prefix, e.__class__.__name__, e))
            raise
    return _wrap_as_new(func, wrapped)

def _format_arg_value(arg_val):
    '''Return a string representing a (name, value) pair.

    >>> _format_arg_value(('x', (1, 2, 3)))
    'x=(1, 2, 3)'

    Copied from: http://wordaligned.org/articles/echo
    '''
    arg, val = arg_val
    return '{}={}'.format(arg, val)
