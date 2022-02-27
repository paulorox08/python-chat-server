import signal
import sys
import socket
import threading
import base64
import time

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#user_ls = [['U1', 'MQ=='], ['U2', 'Mg=='], ['U3', 'Mw==']]
#channel_ls = [['C',[]],['D',[]]]
global user_ls
user_ls = []
global channel_ls
channel_ls = []
global conn_ls
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
        return 'RESULT LOGIN 0\n'
    password = base64.b64encode(password.encode()).decode()
    for user in user_ls:
        if user[0] == username and user[1] == password:
            if conn_ls:
                for conn in conn_ls:
                    if user[0] == conn[0]:
                        return 'RESULT LOGIN 0\n'
                conn_ls.append([username, current_conn])
                return 'RESULT LOGIN 1\n'
            else:
                conn_ls.append([username, current_conn])
                return 'RESULT LOGIN 1\n'
    return 'RESULT LOGIN 0\n'


def create_acc(username, password):
    password = base64.b64encode(password.encode()).decode()
    for user in user_ls:
        # Check existed user
        if user[0] == username:
            return 'RESULT REGISTER 0\n'
    user_ls.append([username,password])
    return 'RESULT REGISTER 1\n'


def create_channel(channel_name, current_user):
    if current_user == '':
        return 'RESULT CREATE '+ channel_name +' 0'+'\n'
    for channel in channel_ls:
        # Check existed channel
        if channel[0] == channel_name:
            return 'RESULT CREATE '+ channel_name +' 0'+'\n'
    channel_ls.append([channel_name, []])
    return 'RESULT CREATE ' + channel_name + ' 1' + '\n'


def join_channel(channel_name, current_user):
    if current_user == '':
        return f'RESULT JOIN {channel_name} 0\n'
    for channel in channel_ls:
        # Check existed channel
        if channel[0] == channel_name:
            for user_in_channel in channel[1]:
                # Check existed user in channel
                if user_in_channel == current_user:
                    return f'RESULT JOIN {channel_name} 0\n'
            channel[1].append(current_user)
            return f'RESULT JOIN {channel_name} 1\n'
    return f'RESULT JOIN {channel_name} 0\n'


def send_channel_msg(channel_name, message, current_user):
    if current_user == '':
        return "Error. Something is wrong\n"
    is_sent = 0
    for channel in channel_ls:
        # Check existed channel
        if channel[0] == channel_name:
            for user_in_channel in channel[1]:
                # Check existed user in channel
                if user_in_channel == current_user:
                    for user_to_send in channel[1]:
                        for conn in conn_ls:
                            if conn[0] == user_to_send:
                                output = f"RECV {current_user} {channel_name} {message}\n"
                                conn[1].send(output.encode(FORMAT))
                                is_sent = 1
                                break
                    return True
            return f'You are not a member of the {channel_name} channel'
    return 'Error. Something is wrong.\n'

def retrieve_channel():
    if len(channel_ls) == 0:
        return 'RESULT CHANNELS \n'
    msg1 = ''
    for channel in channel_ls:
        msg1 = msg1 + channel[0] + ', '
    msg = 'RESULT CHANNELS ' + msg1[:-2] + '\n'
    return msg


def handle_client(conn):
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
                        conn.send(result.encode(FORMAT))
                        if result == 'RESULT LOGIN 1\n':
                            current_user = msg.split(' ')[1]
                            current_conn = conn
                    elif command == 'REGISTER':
                        result = create_acc(msg.split(' ')[1], msg.split(' ')[2])
                        conn.send(result.encode(FORMAT))
                    elif command == 'CREATE':
                        result = create_channel(msg.split(' ')[1].strip(),current_user)
                        conn.send(result.encode(FORMAT))
                    elif command == 'JOIN':
                        result = join_channel(msg.split(' ')[1].strip(),current_user)
                        conn.send(result.encode(FORMAT))
                    elif command == 'SAY':
                        first_part,channel_name, message = msg.split(' ', 2)
                        result = send_channel_msg(channel_name, message.strip(), current_user)
                        if result != True:
                            conn.send(result.encode(FORMAT))
                    elif command == 'CHANNELS':
                        result = retrieve_channel()
                        conn.send(result.encode(FORMAT))
                    elif command == 'QUIT':
                        print(f'Someone has left')
                        break
                    elif command == 'CLEAR':
                        user_ls.clear()
                        channel_ls.clear()
                        conn_ls.clear()
                        result = 'CLEAR 1'
                        conn.send(result.encode(FORMAT))

            conn.close()

    except ConnectionResetError:
        print('error')
        #conn_ls.remove([current_user,current_conn])
        current_conn.send('error'.encode(FORMAT))
        daemon_quit == False
        conn.close()
        print(f'Someone has left')


class ClientThread(threading.Thread):
    def __init__(self, connstream):
        threading.Thread.__init__(self)
        self.conn = connstream

    def run(self):
        handle_client(self.conn)

def run_server():
    global daemon_quit
    try:
        if len(sys.argv) > 1:
            PORT = int(sys.argv[1])
        else:
            PORT = 5050
        SERVER = socket.gethostbyname(socket.gethostname())
    except ValueError:
        print('Invalid port number')
        quit()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER, PORT))
        server.listen()

        while daemon_quit == True:
            conn, addr = server.accept()
            ClientThread(conn).start()

        # make sure all threads are done
        for th in threading.enumerate():
            if th != threading.current_thread():
                th.join()

def run():
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Call your own functions from within
    # the run() funcion
    run_server()



if __name__ == '__main__':
    run()
