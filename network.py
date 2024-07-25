import socket
import threading
import json
import time

data_size = 512

def start_thread(target, args=()):
    threading.Thread(target=target, args=args).start()

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive(socket_obj):
    try: return json.loads(receive_raw(socket_obj).decode().split('\n')[0])
    except Exception as e:
        print(e)
        return None

def send(client_obj, data):
    client = client_obj
    if isinstance(client_obj, Client):
        client = client_obj.client
    
    send_raw(client, json.dumps({**data, 'timestamp': time.time()}).encode() + b'\n')

def receive_raw(socket_obj):
    return socket_obj.recv(data_size)

def send_raw(socket_obj, data):
    socket_obj.sendall(data)

HOST = '10.0.0.237'
PORT = 55555

class Server:
    def __init__(self):
        self.server = create_socket()
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        print("Server is listening...")
        self.clients = []
        client_id = 0
        while True:
            client, address = self.server.accept()
            self.clients.append(client)
            print("Connection established with", address)
            start_thread(self.client_thread, (client, client_id))
            client_id += 1


    def client_thread(self, client, id):
        self.setup_client_id(client, id)
        while True:
            data = receive_raw(client)
            print(data)
            if data:
                [send_raw(c, data) for c in self.clients if c != client]
    

    def setup_client_id(self, client, id):
        is_setup_complete = False
        while is_setup_complete == False:
            print('setting up')
            data = receive(client)
            if 'is_setup_complete' in data:
                is_setup_complete = data['is_setup_complete']
            send(client, {'client_id': id})
        print('setup_complete')


class Client:
    def __init__(self, update_game_state):
        self.update_game_state = update_game_state
        self.client_id = 100
        self.client = create_socket()
        self.client.connect((HOST, PORT))
        start_thread(self.client_thread)

    def client_thread(self):
        self.setup_client_id()
        while True:
            client_state = receive(self.client)
            print(2, client_state)
            if client_state:
                self.update_game_state(client_state)
    
    def setup_client_id(self):
        self.send({})
        is_setup_complete = False
        while is_setup_complete == False:
            print('setting up')
            setup = receive(self.client)
            if 'client_id' in setup:
                self.client_id = setup['client_id']
                is_setup_complete = True
                comfirm_data = {'is_setup_complete': is_setup_complete}
                send(self.client, comfirm_data)
        print('setup complete')

    def send(self, data):
        send(self.client, data)
    
    def is_setup_complete(self):
        return self.client_id != 100