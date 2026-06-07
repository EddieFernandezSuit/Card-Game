import socket
import threading
import time
import json


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
        """Receive exactly one newline-delimited JSON message.

        TCP is a stream, so we keep a per-socket buffer and extract complete
        messages delimited by '\n'.
        """
        try:
            if not hasattr(self, "_buffers"):
                self._buffers = {}
            buf = self._buffers.get(socket_obj, b"")

            while True:
                chunk = socket_obj.recv(4096)
                if not chunk:
                    # Socket closed
                    self._buffers[socket_obj] = b""
                    return None

                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if not line:
                        continue
                    payload = line.decode("utf-8")
                    obj = json.loads(payload)
                    self._buffers[socket_obj] = buf
                    return obj

                self._buffers[socket_obj] = buf

        except Exception as e:
            print(e)
            return None

    def send(self, socket_obj: socket.socket, data: dict):
        if data:
            msg = {**data, 'timestamp': time.time()}
            raw = (json.dumps(msg) + "\n").encode("utf-8")
            socket_obj.sendall(raw)



class Server(NetworkObject):
    def __init__(self, port=PORT):
        self.clients: list[socket.socket] = []
        self.rooms = []
        self.current_port = port

        self._clients_lock = threading.Lock()
        self._rooms_lock = threading.Lock()

        super().__init__(port=PORT)

    def remove_client_everywhere(self, client: socket.socket):
        # Remove from global client list
        with self._clients_lock:
            if client in self.clients:
                self.clients.remove(client)

        # Remove from any room
        with self._rooms_lock:
            for room in self.rooms:
                if client in room['clients']:
                    room['clients'] = [c for c in room['clients'] if c != client]

    def on_thread(self):

        client_id = 0
        while True:
            client, address = self.client.accept()
            with self._clients_lock:
                self.clients.append(client)
            print("Connection established with", address)
            self.start_thread(self.client_thread, (client, client_id))
            client_id += 1


    def send_all(self, msg_obj):
        with self._clients_lock:
            clients_snapshot = list(self.clients)
        for c in clients_snapshot:
            self.send(c, msg_obj)


    def client_thread(self, client: socket.socket, id):
        self.send(client, {'client_id': id})
        this_clients_room = None

        def send_room(msg_obj):
            # Snapshot room clients to avoid concurrent mutation
            with self._rooms_lock:
                room_clients_snapshot = list(this_clients_room['clients'])
            for c in room_clients_snapshot:
                if c != client:
                    self.send(c, msg_obj)


        while True:
            try:
                # msg_obj has this format: {'action': 'data', 'timestamp': 1234567890.123}
                msg_obj = self.receive(client)
                print('msg_obj:', msg_obj)
                if not msg_obj:
                    break
                if 'create_room' in msg_obj:
                    room_id = len(self.rooms)
                    self.rooms.append({'room_id': room_id, 'clients': []})
                    self.send_all({'room_id': room_id})
                elif 'get_rooms' in msg_obj:
                    room_ids = [room['room_id'] for room in self.rooms]
                    self.send(client, {'room_ids': room_ids})
                elif 'join_room' in msg_obj:
                    room_id = msg_obj['join_room']
                    this_clients_room = self.rooms[room_id]

                    if client in this_clients_room['clients']:
                        continue

                    this_clients_room['clients'].append(client)
                    if len(this_clients_room['clients']) == 2:
                        for c in this_clients_room['clients']:
                            self.send(c, {'all_clients_connected': ''})
                elif this_clients_room:
                    send_room(msg_obj)
            except ConnectionError:
                # Any socket failure: drop the client + stop this thread
                print(f"Connection issue with client {id}")
                self.remove_client_everywhere(client)
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

