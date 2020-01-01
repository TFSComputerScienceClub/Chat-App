'''
Commands for users to use in the server.
'''
from Commands import Commands


# Returns tuple, (returns_str:bool,function)
def handle_message(user_message, client_from):
    user_message = user_message.strip()

    message_content = user_message[user_message.find(':') + 1:].strip()  # Removes name from command

    if message_content.find('/') != 0:
        return False, None

    params = message_content.split(' ')
    command = params[0]
    params = params[1:]

    # print('message_content =' + command, ' params = ', params)

    if command == '/users':

        return True, Commands.users()
    elif command == '/kick':

        return True, Commands.kick(*params, client_from)
    elif command == '/login':

        return True, Commands.login(*params, client_from)

    return False, None
