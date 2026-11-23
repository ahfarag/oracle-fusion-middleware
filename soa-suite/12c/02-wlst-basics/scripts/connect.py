# Connect to the Integrated Server using stored credentials
connect(userConfigFile='/u01/oracle/.wlst/user.config',
        userKeyFile='/u01/oracle/.wlst/user.key',
        url='t3://localhost:7101')

state('DefaultServer')

disconnect()
