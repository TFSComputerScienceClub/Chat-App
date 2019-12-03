import socket
import threading

sock = None
ip = '192.168.0.13'
port = 25567

'''
Read Server.py docstrings for further information
'''


def connect_to(ip_, port_):
    sock = socket.socket()
    try:
        sock.connect((ip_, port_))
    except Exception as e:
        print(e)
    return sock


def listen(sock):
    while True:
        msg = sock.recv(1000).decode()
        print('message received from server == ', msg)


def send(sock, msg: str):
    sock.send(msg.encode())


client_sock = connect_to(ip, port)
t1 = threading.Thread(target=listen, args={client_sock})
t1.start()

while True:
    msg = input('Enter message to server:\n')
    print('sending "{}"'.format(msg))
    send(client_sock, msg)
