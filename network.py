import socket
import threading
import time
import pickle


def start_thread(target, args=()):
    threading.Thread(target=target, args=args).start()

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive(socket_obj):
    # try: return pickle.loads(receive_raw(socket_obj).decode().split('\n')[0])
    try: return pickle.loads(receive_raw(socket_obj))
    except Exception as e:
        print(e)
        return None

def send(client_obj, data):
    client = client_obj
    if isinstance(client_obj, Client):
        client = client_obj.client
    
    # send_raw(client, pickle.dumps({**data, 'timestamp': time.time()}) + b'\n')
    send_raw(client, pickle.dumps({**data, 'timestamp': time.time()}))

def receive_raw(socket_obj):
    DATA_SIZE = 512
    return socket_obj.recv(DATA_SIZE)

def send_raw(socket_obj, data):
    socket_obj.sendall(data)

# HOST = '172.232.161.132'
# HOST = '10.0.0.237'
HOST = ''
PORT = 7777


class Server:
    def __init__(self):
        self.server = create_socket()
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        print("Server is listening...")
        self.clients = []
        while True:
            client, address = self.server.accept()
            self.clients.append(client)
            print("Connection established with", address)
            start_thread(self.client_thread, (client, 0))
            if self.check_all_clients_connected():
                self.on_all_clients_connected()

    def client_thread(self, client, id):
        self.setup_client_id(client)
        while True:
            data = receive_raw(client)
            if data:
                [send_raw(c, data) for c in self.clients if c != client]
    
    def setup_client_id(self, client):
        client_id = len(self.clients) - 1
        send(client, {'client_id': client_id})

    def check_all_clients_connected(self):
        TOTAL_NUM_CLIENTS = 2
        if len(self.clients) == TOTAL_NUM_CLIENTS:
            return True
        return False

    def on_all_clients_connected(self):
        for client in self.clients:
            send(client, {'all_clients_connected': True})

class Client:
    def __init__(self, update_game_state, on_client_connect = lambda : 0):
        self.update_game_state = update_game_state
        self.client_id = 100
        self.is_all_clients_connected = False
        self.on_client_connected = self.all_clients_connected
        self.on_client_connect = on_client_connect
        self.client = create_socket()
        self.client.connect((HOST, PORT))
        start_thread(self.client_thread)

    def client_thread(self):
        self.setup_client_id()
        while True:
            client_state = receive(self.client)
            print('client thread:', client_state)
            if client_state:
                self.update_game_state(client_state)

    def setup_client_id(self):
        data = receive(self.client)
        if 'client_id' in data:
            self.client_id = data['client_id']
            print(f'Client ID: {self.client_id}')
        data = receive(self.client)
        if 'all_clients_connected' in data:
            self.all_clients_connected()

    def send(self, data):
        send(self.client, data)
    
    def all_clients_connected(self):
        self.is_all_clients_connected = True
        self.on_client_connect()