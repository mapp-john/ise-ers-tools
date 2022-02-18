# Import Required Modules
import os,\
        re,\
        sys,\
        csv,\
        json,\
        socket,\
        random,\
        netaddr,\
        netmiko,\
        getpass,\
        requests,\
        warnings,\
        traceback

# Disable SSL warning
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
# Disable SSL warning
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


#
#
# Define Password Function
def define_password():
    password = None
    while not password:
        password = getpass.getpass('Please Enter Password: ')
        passwordverify = getpass.getpass('Re-enter Password to Verify: ')
        if not password == passwordverify:
            print('Passwords Did Not Match Please Try Again')
            password = None
    return password





#
#
#
# Deploy Pending FTDs
def bulk_delete_internal_user(server,session):
    print ('''
***********************************************************************************************
*                             Bulk Delete Internal Users                                      *
*_____________________________________________________________________________________________*
*                                                                                             *
* USER INPUT NEEDED:                                                                          *
*                                                                                             *
*  1. Enter ERS API filter for internal users                                                 *
*       example: identityGroup.CONTAINS.DELETE_ME                                             *
*                                                                                             *
***********************************************************************************************
''')

    user_filter = input('Please Enter ERS API Filter: ').strip()
    users = None

    # Collect users to delete
    try:
        # REST call with SSL verification turned off:
        url = f'{server}/ers/config/internaluser?filter={user_filter}'
        r = session.get(url, verify=False)
        status_code = r.status_code
        resp = r.text
        print(f'Status code is: {status_code}')
        if status_code == 200:
            users = [
                {
                'id': u['id'],
                'name': u['name']
                }
            for u in r.json()['SearchResult']['resources']
            ]
        else :
            print(f'Error occurred in GET --> {json.dumps(r.json(),indent=4)}')
            r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print (f'Error in connection --> {traceback.format_exc()}')
    finally:
        try:
            if r: r.close()
        except:
            None

    if not users:
        print(f'No Users Found; filter={user_filter}')
        return
    # Print filtered users
    print(f'Users To Be Deleted:\n{json.dumps(users,indent=4)}')

    while True:
        choice = input('Would You Like To Delete The Filtered Users Above? [y/N]: ').lower()
        if choice in (['yes','ye','y']):
            traffic_int = True
            break
        elif choice in (['no','n','']):
            return
        else:
            print('Invalid Selection...\n')


    # Delete users
    for u in users:
        try:
            # REST call with SSL verification turned off:
            url = f'{server}/ers/config/internaluser/{u["id"]}'
            r = session.delete(url, verify=False)
            status_code = r.status_code
            resp = r.text
            print(f'Status code is: {status_code}')
            if status_code == 204:
                print(f'User Deleted --> {u["name"]}')
            else :
                print(f'Error occurred in Deleted --> {resp}')
                r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print (f'Error in connection --> {traceback.format_exc()}')
        finally:
            try:
                if r: r.close()
            except:
                None






#
#
#
# Run Script if main
if __name__ == "__main__":
    #
    #
    #
    # Initial input request
    print ('''
***********************************************************************************************
*                                                                                             *
*                   Cisco ISE ERS API Tools (Written for Python 3.6+)                        *
*                                                                                             *
***********************************************************************************************
*                                                                                             *
* USER INPUT NEEDED:                                                                          *
*                                                                                             *
*  1. FQDN for ISE server (hostname.domain.com)                                               *
*                                                                                             *
*  2. API Username                                                                            *
*                                                                                             *
*  3. API Password                                                                            *
*                                                                                             *
***********************************************************************************************
''')

    Test = False
    while not Test:
        # Request FMC server FQDN
        server = input('Please Enter ISE fqdn: ').lower().strip()

        # Validate FQDN
        if server[-1] == '/':
            server = server[:-1]
        if '//' in server:
            server = server.split('//')[-1]

        # Perform Test Connection To FQDN
        s = socket.socket()
        print(f'Attempting to connect to {server} on port 9060')
        try:
            s.connect((server, 9060))
            print(f'Connecton successful to {server} on port 9060')
            Test = True
        except:
            print(f'Connection to {server} on port 9060 failed: {traceback.format_exc()}\n\n')

    # Create Request Session
    session = requests.session()

    # Adding HTTPS to Server for URL
    server = f'https://{server}:9060'
    session.headers = {'Content-Type': 'application/json','Accept': 'application/json'}

    # Request Username and Password without showing password in clear text
    username = input('Please Enter API Username: ').strip()
    password = define_password()

    session.auth = (username,password)
    print ('''
***********************************************************************************************
*                                                                                             *
* TOOLS AVAILABLE:                                                                            *
*                                                                                             *
*  1. Basic URL GET                                                                           *
*                                                                                             *
*  2. Bulk Delete Internal Users                                                              *
*                                                                                             *
***********************************************************************************************
''')

    #
    #
    #
    # Run script until user cancels
    while True:
        Script = False
        while not Script:
            script = input('Please Select Tool: ')
            if script == '1':
                Script = True
                blank_get(server,session)
            elif script == '2':
                Script = True
                bulk_delete_internal_user(server,session)
            else:
                print('INVALID ENTRY... ')

        # Ask to end the loop
        print ('''
***********************************************************************************************
*                                                                                             *
* TOOLS AVAILABLE:                                                                            *
*                                                                                             *
*  1. Basic URL GET                                                                           *
*                                                                                             *
*  2. Bulk Delete Internal Users                                                              *
*                                                                                             *
***********************************************************************************************
''')
        Loop = input('*\n*\nWould You Like To use another tool? [y/N]').lower()
        if Loop not in (['yes','ye','y','1','2']):
            break













