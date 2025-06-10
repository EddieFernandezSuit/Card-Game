import socket
import threading
import time
import pickle

# class Connection():
#     def start_thread(target, args=()):
#         threading.Thread(target=target, args=args).start()
    
#     def create_socket():
#         return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
#     def receive(socket_obj):
#         # try: return pickle.loads(receive_raw(socket_obj).decode().split('\n')[0])
#         try: return pickle.loads(receive_raw(socket_obj))
#         except Exception as e:
#             print(e)
#             return None

#     def send(client_obj, data):
#         client = client_obj
#         if isinstance(client_obj, Client):
#             client = client_obj.client
        
#         # send_raw(client, pickle.dumps({**data, 'timestamp': time.time()}) + b'\n')
#         send_raw(client, pickle.dumps({**data, 'timestamp': time.time()}))

#     def receive_raw(socket_obj):
#         DATA_SIZE = 512
#         return socket_obj.recv(DATA_SIZE)

#     def send_raw(socket_obj, data):
#         socket_obj.sendall(data)


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
    
    # try:
    # print(data,client)
    if data:
        send_raw(client, pickle.dumps({**data, 'timestamp': time.time()}))
    # except:
    #     print(f"Unable to reach client with socket {client}")

def receive_raw(socket_obj):
    DATA_SIZE = 512
    return socket_obj.recv(DATA_SIZE)

def send_raw(socket_obj, data):
    socket_obj.sendall(data)

def get_ip():
    import socket
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)

# HOST = '172.232.161.132'
# HOST = '67.185.216.120'
# HOST = '54.196.161.61'
# HOST = '44.226.145.213'
# HOST = '172.20.20.20'
EDDIE_IP = '10.0.0.237'
RACHEL_IP = '10.5.0.2'
HOST = EDDIE_IP
PORT = 7777


class Server:
    def __init__(self, port):
        self.server = create_socket()
        self.server.bind((HOST, port))
        self.server.listen(5)
        print("Server is listening...")
        self.clients = []
        self.rooms = []
        self.current_port = port
        start_thread(self.server_thread)

    def server_thread(self):
        client_id = 0
        while True:
            client, address = self.server.accept()
            self.clients.append(client)
            print("Connection established with", address)
            start_thread(self.client_thread, (client, client_id))
            client_id += 1
    
    def send(self, client, msg):
        # try:
        send(client, msg)
        # except:
        #     print(f"Unable to reach client with socket {client}")
        #     input('asdfa')
            
        #     if client in self.clients:
        #         self.clients.remove(client)

    def send_all(self, msg_obj):
        [self.send(c, msg_obj) for c in self.clients]

    def client_thread(self, client, id):
        self.send(client, {'client_id': id})
        this_clients_room = None

        def send_room(msg_obj):
            [self.send(c, msg_obj) for c in this_clients_room['clients'] if c != client]

        while True:
            try:
                msg_obj = receive(client)
                if not msg_obj: break
            except ConnectionError:
                print(f"Connection from client {id} has been lost.")
                if client in self.clients:
                    self.clients.remove(client)
                break
            try:
                if this_clients_room:
                    send_room(msg_obj)
                else:
                    if msg_obj:
                        if 'get_rooms' in msg_obj:
                            room_ids = [room['room_id'] for room in self.rooms]
                            self.send(client, {'room_ids': room_ids})
                        if 'create_room' in msg_obj:
                            room_id = len(self.rooms)
                            self.rooms.append({'room_id': room_id, 'clients': []})
                            msg = {'room_id': room_id}
                            self.send_all(msg)
                        if 'join_room' in msg_obj:
                            room_id = msg_obj['join_room']
                            this_clients_room = self.rooms[room_id]
                            this_clients_room['clients'].append(client)
                            if len(this_clients_room['clients']) == 2:
                                for c in this_clients_room['clients']:
                                    self.send(c, {'all_clients_connected': ''})
            except ConnectionError:
                print(f"Unable to reach client with socket {client}")
                
                if client in self.clients:
                    self.clients.remove(client)
                    print('this return')
                return

class Client:
    def __init__(self, update_game_state, on_client_connect = lambda : 0, port = PORT, wait_for_clients=True):
        self.update_game_state = update_game_state
        self.client_id = 100
        self.on_client_connect = on_client_connect
        self.client = create_socket()
        self.client.connect((HOST, port))
        self.room = None
        start_thread(self.client_thread)

    def client_thread(self):
        while True:
            try:
                msg = receive(self.client)
                if not msg: break
                print('client thread:', msg)
                
                if 'client_id' in msg:
                    self.client_id = msg['client_id']

                self.update_game_state(msg)
            except ConnectionError as e:
                print('Connection Error', e)
                return

    def send(self, data):
        send(self.client, data)