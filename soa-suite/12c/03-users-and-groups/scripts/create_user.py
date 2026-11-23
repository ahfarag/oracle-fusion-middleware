# Create a group and a user, and add the user to the group
# Usage: wlst.sh create_user.py [-u <user>] [-g <group>] [-p <password>]
# Defaults: user hello_user, group HelloUsers. Without -p, the script asks for the password.
import getopt
import sys
from jarray import array
from java.lang import Object, String, System

USAGE = 'Usage: $ORACLE_HOME/oracle_common/common/bin/wlst.sh create_user.py [-u <user>] [-g <group>] [-p <password>]'

user_name = 'hello_user'
group_name = 'HelloUsers'
password = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'u:g:p:')
except getopt.GetoptError, e:
    print(str(e))
    print(USAGE)
    exit(exitcode=1)
if args:
    print('Unexpected argument: ' + args[0])
    print(USAGE)
    exit(exitcode=1)
for opt, value in opts:
    if opt == '-u':
        user_name = value
    elif opt == '-g':
        group_name = value
    elif opt == '-p':
        password = value


def read_password():
    console = System.console()
    if console is None:
        raise Exception('No console to read the password. Pass it with -p.')
    no_args = array([], Object)  # WLST's Jython 2.2 has no varargs
    first = String(console.readPassword('Password for ' + user_name + ': ', no_args))
    second = String(console.readPassword('Confirm password: ', no_args))
    if not first.equals(second):
        raise Exception('Passwords do not match.')
    return str(first)


connect(userConfigFile='/u01/oracle/.wlst/user.config',
        userKeyFile='/u01/oracle/.wlst/user.key',
        url='t3://localhost:7101')

try:
    atn = cmo.getSecurityConfiguration().getDefaultRealm() \
             .lookupAuthenticationProvider('DefaultAuthenticator')

    if atn.groupExists(group_name):
        print('Group ' + group_name + ' already exists')
    else:
        atn.createGroup(group_name, 'Created by create_user.py')
        print('Created group ' + group_name)

    if atn.userExists(user_name):
        print('User ' + user_name + ' already exists, password not changed')
    else:
        if password is None:
            password = read_password()
        atn.createUser(user_name, password, 'Created by create_user.py')
        print('Created user ' + user_name)

    if not atn.isMember(group_name, user_name, 0):
        atn.addMemberToGroup(group_name, user_name)

    if atn.isMember(group_name, user_name, 0):
        print(user_name + ' is a member of ' + group_name)
finally:
    disconnect()
