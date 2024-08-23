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
# HOST = '67.185.216.120'
# HOST = '54.196.161.61'
# HOST = '44.226.145.213'
HOST = '10.0.0.237'
# HOST = ''
PORT = 7777

class Server:
    def __init__(self, port):
        self.server = create_socket()
        self.server.bind((HOST, port))
        self.server.listen(5)
        print("Server is listening...")
        self.clients = []
        self.server_ports = []
        self.servers = []
        self.current_port = port
        self.total_clients = 1
        start_thread(self.server_thread)

    def server_thread(self):
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
            data = receive(client)
            if data:
                if 'port' in data:
                    self.current_port += 1
                    self.server_ports.append(self.current_port)
                    self.servers.append(Server(self.current_port))
                    [send(c, {'port': self.current_port}) for c in self.clients]
                    continue
                # if 'create_server' in data:
                    # self.other_servers.append(Server(self.current_port))
                    # continue
                # if 'port' not in data and 'create_server' not in data:
                [send(c, data) for c in self.clients if c != client]
    
    def setup_client_id(self, client):
        print('here')
        client_id = len(self.clients) - 1
        send(client, {'client_id': client_id})
        print(self.server_ports)
        if self.server_ports:
            send(client, {'ports': self.server_ports})
            

    def check_all_clients_connected(self):
        if len(self.clients) == self.total_clients:
            return True
        return False

    def on_all_clients_connected(self):
        for client in self.clients:
            send(client, {'all_clients_connected': True})

class Client:
    def __init__(self, update_game_state, on_client_connect = lambda : 0, port = PORT, wait_for_clients=True):
        self.update_game_state = update_game_state
        self.client_id = 100
        self.is_all_clients_connected = False
        self.on_client_connected = self.all_clients_connected
        self.on_client_connect = on_client_connect
        self.client = create_socket()
        self.client.connect((HOST, port))
        self.wait_for_clients = wait_for_clients
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
        
        if self.wait_for_clients:
            data = receive(self.client)
            if 'all_clients_connected' in data:
                self.all_clients_connected()

    def send(self, data):
        send(self.client, data)
    
    def all_clients_connected(self):
        self.is_all_clients_connected = True
        self.on_client_connect()