import socket
import threading
import time
import pickle
import struct

def get_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)

EDDIE_IP = '10.0.0.237'
RACHEL_IP = '24.17.185.236'
HOME_IP = '127.0.0.1'
HOST = HOME_IP
PORT = 8000


class NetworkObject:
    # TCP is a byte stream; we must frame messages.
    # Protocol: [4-byte big-endian unsigned length][payload bytes]
    HEADER_SIZE = 4

    def __init__(self, port=PORT):
        self.client = self.create_socket()
        if isinstance(self, Server):
            self.client.bind((HOST, port))
            self.client.listen(5)
            print("Server is listening...")

        elif isinstance(self, Client):
            self.client.connect((HOST, port))

        self.start_thread(self.on_thread)

    def create_socket(self) -> socket.socket:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client_socket

    def start_thread(self, target, args=()):
        threading.Thread(target=target, args=args).start()

    def receive(self, socket_obj: socket.socket):
        try:
            DATA_SIZE = 512
            raw_data = socket_obj.recv(DATA_SIZE)
            obj = pickle.loads(raw_data)
            return obj
        except Exception as e:
            print(e)
            return None

    def send(self, socket_obj: socket.socket, data: dict):
        if data:
            pickled_data = pickle.dumps({**data, 'timestamp': time.time()})
            socket_obj.sendall(pickled_data)


class Server(NetworkObject):
    def __init__(self, port=PORT):
        self.clients: list[socket.socket] = []
        self.rooms = []
        self.current_port = port
        super().__init__(port=PORT)

    def on_thread(self):
        client_id = 0
        while True:
            client, address = self.client.accept()
            self.clients.append(client)
            print("Connection established with", address)
            self.start_thread(self.client_thread, (client, client_id))
            client_id += 1

    def send_all(self, msg_obj):
        [self.send(c, msg_obj) for c in self.clients]

    def client_thread(self, client: socket.socket, id):
        self.send(client, {'client_id': id})
        this_clients_room = None

        def send_room(msg_obj):
            [self.send(c, msg_obj) for c in this_clients_room['clients'] if c != client]

        while True:
            try:
                # msg_obj has this format: {'action': 'data', 'timestamp': 1234567890.123}
                msg_obj = self.receive(client)
                print('msg_obj:', msg_obj)
                if not msg_obj:
                    break
            except ConnectionError:
                print(f"Connection from client {id} has been lost.")
                if client in self.clients:
                    self.clients.remove(client)
                break
            try:
                if 'create_room' in msg_obj:
                    room_id = len(self.rooms)
                    self.rooms.append({'room_id': room_id, 'clients': []})
                    msg = {'room_id': room_id}
                    self.send_all(msg)
                elif 'get_rooms' in msg_obj:
                    room_ids = [room['room_id'] for room in self.rooms]
                    self.send(client, {'room_ids': room_ids})
                elif 'join_room' in msg_obj:
                    room_id = msg_obj['join_room']
                    this_clients_room = self.rooms[room_id]
                    this_clients_room['clients'].append(client)
                    if len(this_clients_room['clients']) == 2:
                        for c in this_clients_room['clients']:
                            self.send(c, {'all_clients_connected': ''})
                elif this_clients_room:
                    send_room(msg_obj)
            except ConnectionError:
                print(f"Unable to reach client with socket {client}")

                if client in self.clients:
                    self.clients.remove(client)
                    print('this return')
                return


class Client(NetworkObject):
    def __init__(self, port=PORT, update_game_state=lambda x: 0, on_client_connect=lambda: 0, wait_for_clients=True):
        self.client_id = 100
        self.on_client_connect = on_client_connect
        self.update_game_state = update_game_state
        self.room = None
        super().__init__(port=PORT)

    def on_thread(self):
        while True:
            try:
                msg = self.receive(self.client)
                if not msg:
                    break
                print('client thread:', msg)

                if 'client_id' in msg:
                    self.client_id = msg['client_id']

                self.update_game_state(msg)
            except ConnectionError as e:
                print('Connection Error', e)
                return

    def send(self, data):
        super().send(self.client, data)

