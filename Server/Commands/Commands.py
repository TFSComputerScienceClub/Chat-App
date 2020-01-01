server_reference = None
SERVER_PASSWORD = 'admin123'
help_dict = {'/kick': 'Kick user from server.', '/users': 'Lists all connected users',
             'login': 'Login for administrative control over the server, including banning, kicking, '
                      'uploading files, and shutting down the server remotely.'}


def set_server_reference(server):
    global server_reference
    server_reference = server


def help_list():
    pass


def login(password, client_from):
    if password == SERVER_PASSWORD:

        client_from.admin = True
        return 'Access Granted!'
    else:

        return 'Incorrect password. Access Denied.'


def kick(user, client_from):
    print('kicking')
    if client_from.admin:
        kicked = False
        for client in server_reference.clients:
            if client.username == user:
                print('kicking ', user)
                client.disconnect('You Have been kicked by  Admin')
                kicked = True

        # Return kicked status..
        if kicked:
            return 'Kicked user ' + user
        else:
            return 'Could not find ' + user
    else:
        return 'You do not have permissions to kick users!'


# Returns all connected users.
def users():
    client_names = []
    for client in server_reference.clients:
        client_names.append(client.username)
    return str(client_names)
