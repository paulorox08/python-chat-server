import json
from test_server import *


HEADER = 64
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

testcase_ls = []

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())


def clear_data_before_test(client):
    client.send('CLEAR'.encode(FORMAT))
    recv = client.recv(2048).decode(FORMAT)
    if recv != 'CLEAR 1':
        return 'Failed'

def clear_data():
    conn_ls.clear()
    user_ls.clear()
    channel_ls.clear()


def client_register_1():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER U1 1'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        client.send('REGISTER U1 1'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 0\n':
            return 'Failed'
        return 'Passed'


def client_register_2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER 舊字形 1'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        return 'Passed'


def client_login_1():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER U1 1'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        client.send('LOGIN U1 1'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
            return 'Failed'
        return 'Passed'


def client_login_2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('LOGIN U2 2'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 0\n':
            return 'Failed'
        return 'Passed'


def multiple_client_login_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    client_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_2.connect((SERVER, PORT))
    clear_data_before_test(client)
    client.send('REGISTER U1 1'.encode(FORMAT))
    if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
        return 'Failed'
    client.send('LOGIN U1 1'.encode(FORMAT))
    if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
        return 'Failed'
    client_2.send('LOGIN U1 1'.encode(FORMAT))
    if client_2.recv(2048).decode(FORMAT) != 'RESULT LOGIN 0\n':
        return 'Failed'
    return 'Passed'


def client_login_3():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        client.send('LOGIN U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
            return 'Failed'
        client.send('LOGIN U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 0\n':
            return 'Failed'
        return 'Passed'


def client_create_channel_1():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        client.send('LOGIN U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
            return 'Failed'
        client.send('CREATE SOCIAL'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE SOCIAL 1\n':
            return 'Failed'
        return 'Passed'


def client_create_channel_2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        client.send('LOGIN U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
            return 'Failed'
        client.send('CREATE SOCIAL'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE SOCIAL 1\n':
            return 'Failed'
        client.send('CREATE SOCIAL'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE SOCIAL 0\n':
            return 'Failed'
        return 'Passed'

def client_create_channel_3():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('CREATE SOCIAL'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE SOCIAL 0\n':
            return 'Failed'
        return 'Passed'

def client_retrieve_channel_1():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('CHANNELS'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CHANNELS \n':
            return 'Failed'
        return 'Passed'


def client_retrieve_channel_2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        client.send('LOGIN U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
            return 'Failed'
        client.send('CREATE SOCIAL'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE SOCIAL 1\n':
            return 'Failed'
        client.send('CREATE FAMILY'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE FAMILY 1\n':
            return 'Failed'
        client.send('CHANNELS'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CHANNELS SOCIAL, FAMILY\n':
            return 'Failed'
        return 'Passed'


def client_join_1():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        client.send('LOGIN U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
            return 'Failed'
        client.send('CREATE FAMILY'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE FAMILY 1\n':
            return 'Failed'
        client.send('JOIN FAMILY'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT JOIN FAMILY 1\n':
            return 'Failed'
        client.send('JOIN FAMILY'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT JOIN FAMILY 0\n':
            return 'Failed'
        return 'Passed'


def client_join_2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('REGISTER U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
            return 'Failed'
        client.send('LOGIN U3 3'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
            return 'Failed'
        client.send('CREATE FAMILY'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE FAMILY 1\n':
            return 'Failed'
        client.send('JOIN FAMILY'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT JOIN FAMILY 1\n':
            return 'Failed'
        client.send('JOIN SOCIAL'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT JOIN SOCIAL 0\n':
            return 'Failed'
        return 'Passed'

def client_join_3():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER, PORT))
        clear_data_before_test(client)
        client.send('CREATE FAMILY'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT CREATE FAMILY 0\n':
            return 'Failed'
        client.send('JOIN FAMILY'.encode(FORMAT))
        if client.recv(2048).decode(FORMAT) != 'RESULT JOIN FAMILY 0\n':
            return 'Failed'
        return 'Passed'


def client_say_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    clear_data_before_test(client)
    client.send('REGISTER U3 3'.encode(FORMAT))
    if client.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
        return 'Failed'
    client.send('LOGIN U3 3'.encode(FORMAT))
    if client.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
        return 'Failed'
    client.send('CREATE FAMILY'.encode(FORMAT))
    if client.recv(2048).decode(FORMAT) != 'RESULT CREATE FAMILY 1\n':
        return 'Failed'
    client.send('JOIN FAMILY'.encode(FORMAT))
    if client.recv(2048).decode(FORMAT) != 'RESULT JOIN FAMILY 1\n':
        return 'Failed'

    client_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_2.connect((SERVER, PORT))
    client_2.send('REGISTER U4 4'.encode(FORMAT))
    if client_2.recv(2048).decode(FORMAT) != 'RESULT REGISTER 1\n':
        return 'Failed'
    client_2.send('LOGIN U4 4'.encode(FORMAT))
    if client_2.recv(2048).decode(FORMAT) != 'RESULT LOGIN 1\n':
        return 'Failed'
    client_2.send('JOIN FAMILY'.encode(FORMAT))
    if client_2.recv(2048).decode(FORMAT) != 'RESULT JOIN FAMILY 1\n':
        return 'Failed'

    client_2.send('SAY FAMILY HI'.encode(FORMAT))
    recv = client_2.recv(2048).decode(FORMAT)
    if recv != 'RECV U4 FAMILY HI\n':
        return 'Failed'
    recv_2 = client.recv(2048).decode(FORMAT)
    if recv_2 != 'RECV U4 FAMILY HI\n':
        return 'Failed'

    client.send('SAY FAMILY HOW ARE YOU'.encode(FORMAT))
    recv = client.recv(2048).decode(FORMAT)
    if recv != 'RECV U3 FAMILY HOW ARE YOU\n':
        return 'Failed'
    recv_2 = client_2.recv(2048).decode(FORMAT)
    if recv_2 != 'RECV U3 FAMILY HOW ARE YOU\n':
        return 'Failed'

    return 'Passed'

def server_register_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = create_acc('U1', '1')
    if result != 'RESULT REGISTER 1\n':
        return 'Failed'
    result = create_acc('U1', '1')
    if result != 'RESULT REGISTER 0\n':
        return 'Failed'
    return 'Passed'

def server_login_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = login('U1','1','',client)
    if result != 'RESULT LOGIN 0\n':
        return 'Failed'
    return 'Passed'

def server_login_2():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = create_acc('U1','1')
    if result != 'RESULT REGISTER 1\n':
        return 'Failed'
    result = login('U1','1','',client)
    if result != 'RESULT LOGIN 1\n':
        return 'Failed'
    result = login('U1','1','',client)
    if result != 'RESULT LOGIN 0\n':
        return 'Failed'
    return 'Passed'

def multiple_server_login_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = create_acc('U1','1')
    if result != 'RESULT REGISTER 1\n':
        return 'Failed'
    result = create_acc('U2', '2')
    if result != 'RESULT REGISTER 1\n':
        return 'Failed'
    result = login('U1','1','',client)
    if result != 'RESULT LOGIN 1\n':
        return 'Failed'
    result = login('U2','2','',client)
    if result != 'RESULT LOGIN 1\n':
        return 'Failed'
    return 'Passed'

def server_create_channel_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = create_channel('SOCIAL','')
    if result != 'RESULT CREATE SOCIAL 0\n':
        return 'Failed'
    result = create_channel('SOCIAL', 'U1')
    if result != 'RESULT CREATE SOCIAL 1\n':
        return 'Failed'
    result = create_channel('SOCIAL', 'U1')
    if result != 'RESULT CREATE SOCIAL 0\n':
        return 'Failed'
    return 'Passed'

def server_retrieve_channel_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = retrieve_channel()
    if result != 'RESULT CHANNELS \n':
        return 'Failed'
    return 'Passed'

def server_retrieve_channel_2():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = create_acc('U1', '1')
    if result != 'RESULT REGISTER 1\n':
        return 'Failed'
    result = login('U1', '1', '', client)
    if result != 'RESULT LOGIN 1\n':
        return 'Failed'
    result = create_channel('SOCIAL','U1')
    if result != 'RESULT CREATE SOCIAL 1\n':
        return 'Failed'
    result = create_channel('FAMILY','U1')
    if result != 'RESULT CREATE FAMILY 1\n':
        return 'Failed'
    result = retrieve_channel()
    if result != 'RESULT CHANNELS SOCIAL, FAMILY\n':
        return 'Failed'
    return 'Passed'

def server_join_channel_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = create_acc('U1', '1')
    if result != 'RESULT REGISTER 1\n':
        return 'Failed'
    result = login('U1', '1', '', client)
    if result != 'RESULT LOGIN 1\n':
        return 'Failed'
    result = create_channel('SOCIAL','U1')
    if result != 'RESULT CREATE SOCIAL 1\n':
        return 'Failed'
    result = join_channel('SOCIAL', '')
    if result != 'RESULT JOIN SOCIAL 0\n':
        return 'Failed'
    result = join_channel('SOCIAL','U1')
    if result != 'RESULT JOIN SOCIAL 1\n':
        return 'Failed'
    result = join_channel('SOCIAL', 'U1')
    if result != 'RESULT JOIN SOCIAL 0\n':
        return 'Failed'
    result = join_channel('FAMILY', 'U1')
    if result != 'RESULT JOIN FAMILY 0\n':
        return 'Failed'
    return 'Passed'

def server_say_1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clear_data()
    result = create_acc('U1', '1')
    if result != 'RESULT REGISTER 1\n':
        return 'Failed'
    result = login('U1', '1', '', client)
    if result != 'RESULT LOGIN 1\n':
        return 'Failed'
    result = create_channel('SOCIAL','')
    if result != 'RESULT CREATE SOCIAL 1\n':
        return 'Failed'
    result = join_channel('SOCIAL','U1')
    if result != 'RESULT JOIN SOCIAL 1\n':
        return 'Failed'
    result = send_channel_msg('SOCIAL','HI','U1')
    if result != True:
        return 'Failed'
    return 'Passed'

def run():
    testcase_ls.append({client_register_1.__name__: client_register_1()})
    testcase_ls.append({client_register_2.__name__: client_register_2()})
    testcase_ls.append({client_login_1.__name__: client_login_1()})
    testcase_ls.append({client_login_2.__name__: client_login_2()})
    testcase_ls.append({client_login_3.__name__: client_login_3()})
    testcase_ls.append({multiple_client_login_1.__name__: multiple_client_login_1()})
    testcase_ls.append({client_create_channel_1.__name__: client_create_channel_1()})
    testcase_ls.append({client_create_channel_2.__name__: client_create_channel_2()})
    testcase_ls.append({client_create_channel_3.__name__: client_create_channel_3()})
    testcase_ls.append({client_retrieve_channel_1.__name__: client_retrieve_channel_1()})
    testcase_ls.append({client_retrieve_channel_2.__name__: client_retrieve_channel_2()})
    testcase_ls.append({client_join_1.__name__: client_join_1()})
    testcase_ls.append({client_join_2.__name__: client_join_2()})
    testcase_ls.append({client_join_3.__name__: client_join_3()})
    testcase_ls.append({client_say_1.__name__: client_say_1()})
    testcase_ls.append({server_register_1.__name__: server_register_1()})
    testcase_ls.append({server_login_1.__name__: server_login_1()})
    testcase_ls.append({server_login_2.__name__: server_login_2()})
    testcase_ls.append({multiple_server_login_1.__name__: multiple_server_login_1()})
    testcase_ls.append({server_create_channel_1.__name__: server_create_channel_1()})
    testcase_ls.append({server_retrieve_channel_1.__name__: server_retrieve_channel_1()})
    testcase_ls.append({server_retrieve_channel_2.__name__: server_retrieve_channel_2()})
    testcase_ls.append({server_join_channel_1.__name__: server_join_channel_1()})

    export_json()

def export_json():
    f = open("output.json", "w")
    f.write(json.dumps(testcase_ls, indent=2))
    f.close()

if __name__ == '__main__':
    run()
