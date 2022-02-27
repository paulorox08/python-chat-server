import signal
import os
import re
import sys
import socket
import sqlite3
import base64
import json
import multiprocessing

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())

FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#user_ls = [['U1', 'MQ=='], ['U2', 'Mg=='], ['U3', 'Mw==']]
#channel_ls = [['C',[]],['D',[]]]
user_ls = []
channel_ls = []
conn_ls = []


#Use this variable for your loop
daemon_quit = True

#Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True

def login(username, password, current_user, current_conn):
    # Check if user already login
    if username == current_user or current_user != '':
        current_conn.send('RESULT LOGIN 0\n'.encode(FORMAT))
        return 0
    password = base64.b64encode(password.encode()).decode()
    for user in user_ls:
        if user[0] == username and user[1] == password:
            if conn_ls:
                for conn in conn_ls:
                    if user[0] == conn[0]:
                        print('RESULT LOGIN 0')
                        current_conn.send('RESULT LOGIN 0\n'.encode(FORMAT))
                        return 0
                conn_ls.append([username, current_conn])
                #print(conn_ls)
                print('RESULT LOGIN 1')
                current_conn.send('RESULT LOGIN 1\n'.encode(FORMAT))
                return 1
            else:
                conn_ls.append([username, current_conn])
                #print(conn_ls)
                print('RESULT LOGIN 1')
                current_conn.send('RESULT LOGIN 1\n'.encode(FORMAT))
                return 1
    print('RESULT LOGIN 0\n')
    current_conn.send('RESULT LOGIN 0\n'.encode(FORMAT))
    return 0


def create_acc(username, password,current_conn):
    password = base64.b64encode(password.encode()).decode()
    for user in user_ls:
        # Check existed user
        if user[0] == username:
            print('RESULT REGISTER 0')
            current_conn.send('RESULT REGISTER 0\n'.encode(FORMAT))
            return 0
    user_ls.append([username,password])
    print('RESULT REGISTER 1')
    current_conn.send('RESULT REGISTER 1\n'.encode(FORMAT))
    return 1


def create_channel(channel_name, current_conn):
    for channel in channel_ls:
        # Check existed channel
        if channel[0] == channel_name:
            print(f'RESULT CREATE {channel_name} 0')
            output = 'RESULT CREATE '+ channel_name +' 0'+'\n'
            current_conn.send(output.encode(FORMAT))
            return 0
    channel_ls.append([channel_name, []])
    print(f'RESULT CREATE {channel_name} 1')
    output = 'RESULT CREATE ' + channel_name + ' 1' + '\n'
    current_conn.send(output.encode(FORMAT))
    return 1


def join_channel(channel_name, current_user, current_conn):
    for channel in channel_ls:
        # Check existed channel
        if channel[0] == channel_name:
            for user_in_channel in channel[1]:
                # Check existed user in channel
                if user_in_channel == current_user:
                    print(f'RESULT JOIN {channel_name} 0\n')
                    output = f'RESULT JOIN {channel_name} 0\n'
                    current_conn.send(output.encode(FORMAT))
                    return 0
            channel[1].append(current_user)
            print(f'RESULT JOIN {channel_name} 1')
            output = 'RESULT JOIN '+ channel_name +' 1'+'\n'
            current_conn.send(output.encode(FORMAT))
            return 1

    print(f'RESULT JOIN {channel_name} 0\n')
    output = f'RESULT JOIN {channel_name} 0\n'
    current_conn.send(output.encode(FORMAT))
    return 0


def send_channel_msg(channel_name, message, current_user,current_conn):
    is_sent = 0
    for channel in channel_ls:
        # Check existed channel
        if channel[0] == channel_name:
            for user_in_channel in channel[1]:
                # Check existed user in channel
                if user_in_channel == current_user:
                    for user_to_send in channel[1]:
                        for conn in conn_ls:
                            # if conn[0] == current_user:
                            #     output = f"RECV {current_user} {channel_name} {message}\n"
                            #     current_conn.send(output.encode(FORMAT))
                            if conn[0] == user_to_send:
                                output = f"RECV {current_user} {channel_name} {message}\n"
                                conn[1].send(output.encode(FORMAT))
                                #current_conn.send(output.encode(FORMAT))
                                print(f"RECV {current_user} {channel_name} {message}")
                                is_sent = 1
                                break

                    return is_sent
            print(f'You are not a member of the {channel_name} channel')
            output = f'You are not a member of the {channel_name} channel'
            current_conn.send(output.encode(FORMAT))
            return (f'You are not a member of the {channel_name} channel', is_sent)

    print(f'RESULT SAY {channel_name} 0')
    #output = f'RESULT SAY {channel_name} 0\n'
    output = '*(customised error, can be anything)\n'
    current_conn.send(output.encode(FORMAT))
    return is_sent

    # try:
    #     members = channels[channel_name]
    #     if client in members:
    #         for cl in members:
    #             cl.send(f"RECV {current_user} {channel_name} {message}".encode())
    #         return ('', True)
    #     else:
    #         return (f'You are not a member of the {channel_name} channel', False)
    #
    # except KeyError:
    #     return ('Channel doesnt exist', False)


def handle_client(conn, addr):
    joined_channels = []
    current_user = ''
    current_conn = []
    global daemon_quit
    try:
        with conn:
            while daemon_quit == True:
                msg = conn.recv(2048).decode(FORMAT)
                if msg:
                    if msg == DISCONNECT_MESSAGE:
                        daemon_quit = False

                    command = msg.split(' ')[0].strip()
                    if command == 'LOGIN':
                        result = login(msg.split(' ')[1], msg.split(' ')[2], current_user, conn)
                        if result == 1:
                            current_user = msg.split(' ')[1]
                            current_conn = conn

                    elif command == 'REGISTER':
                        result = create_acc(msg.split(' ')[1], msg.split(' ')[2],conn)
                    elif command == 'CREATE':
                        result = create_channel(msg.split(' ')[1].strip(),conn)
                    elif command == 'JOIN':
                        result = join_channel(msg.split(' ')[1].strip(),current_user,conn)
                    elif command == 'SAY':
                        first_part,channel_name, message = msg.split(' ', 2)
                        result = send_channel_msg(channel_name, message.strip(), current_user,conn)

                    elif command == 'CHANNELS':
                        msg1 = ''
                        for channel in sorted(channel_ls):
                            msg1 = msg1 + channel[0] + ', '
                        msg = 'RESULT CHANNELS ' + msg1
                        msg = msg[:-2] + '\n'
                        if len(channel_ls) == 0:
                            msg = 'RESULT CHANNELS \n'
                        print(msg)
                        conn.send(msg.encode(FORMAT))
                    elif command == 'QUIT':
                        print(f'{addr} has left the room')
                        return
                    # else:
                    #     temp = ('', False)
                    #     conn.send(json.dumps(temp).encode())

                    # client_status = conn.recv(1024).decode()
                    # if client_status == 'ok':
                    #     break

                # command = conn.recv(2048).decode()
                # client_status = 'no'
                # message = command.split(' ')
                # if not message:
                #     temp = ('', False)
                #     conn.send(message)
                #     conn.send(json.dumps(temp).encode())
                #
                #     client_status = conn.recv(1024).decode()
                #     if client_status == 'ok':
                #         break
                #     continue
                #
                # option = message[0].strip() # LOGIN USERNAME PASSWORD
                # if option == 'LOGIN':
                #     try:
                #         info = re.search('LOGIN (.*) (.*)', command).groups()
                #     except AttributeError:
                #         temp = ('', False)
                #
                #         conn.send(json.dumps(temp).encode())
                #
                #         client_status = conn.recv(1024).decode()
                #         if client_status == 'ok':
                #             break
                #         continue
                #     username, password = info[0].strip(), info[1].strip()
                #     msg = access_db(username, password)
                #     conn.send(json.dumps(msg).encode())
            conn.close()

    except ConnectionResetError:
        print('error')
        #conn_ls.remove([current_user,current_conn])
        current_conn.send('error'.encode(FORMAT))
        daemon_quit == False
        conn.close()
        print(f'{addr} has left')


def run():
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Call your own functions from within
    # the run() funcion
    global daemon_quit
    try:
        PORT = int(sys.argv[1])
        SERVER = socket.gethostbyname(socket.gethostname())
    except ValueError:
        print('Invalid port number')
        quit()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER, PORT))
        server.listen()

        while daemon_quit == True:
            conn, addr = server.accept()
            p = multiprocessing.Process(target=handle_client, args=(conn, addr))
            p.start()

if __name__ == '__main__':
    run()
