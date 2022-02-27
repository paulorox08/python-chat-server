import socket
import multiprocessing
import json
import sys

HEADER = 64
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


def receive(client):

    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            if msg:
                print(msg)
        except (ConnectionAbortedError, OSError):
            print('Goodbye')
            break


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            PORT = int(sys.argv[1])
            SERVER = socket.gethostbyname(socket.gethostname())

        except ValueError:
            print('Invalid port number')
            quit()


        client.connect((SERVER, PORT))
        receive_p = multiprocessing.Process(target=receive, args=(client,))
        p.start()

        while True:
            #print('input your data')
            message_from_client = input()
            if message_from_client == 'QUIT':
                client.send(DISCONNECT_MESSAGE)
                sys.exit(0)
            message = message_from_client.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            #client.send(send_length)
            client.send(message)


except (KeyboardInterrupt, OSError):
    pass
