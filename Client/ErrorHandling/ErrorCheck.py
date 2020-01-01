


def get_client_error(client, exception):
    error = ''
    if client  is None:
        error += 'Socket is not connected!'
        return error
    else:
        error = exception
        return error




