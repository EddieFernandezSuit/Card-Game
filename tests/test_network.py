import pytest
from network import NetworkObject
import json

class FakeSocket:
    def __init__(self, chunks):
        self.chunks = list(chunks)
    
    def recv(self, n):
        if not self.chunks:
            return b""
        
        return self.chunks.pop(0)

class FakeRecorderSocket:
    def __init__(self):
        self.sent = b""
    def sendall(self, data):
        self.sent += data

@pytest.fixture
def network():
    return NetworkObject.__new__(NetworkObject)


def test_receive_single_message():
    net = NetworkObject.__new__(NetworkObject)
    sock = FakeSocket([b'{"action":"create_room"}\n'])
    msg = net.receive(sock)

    assert msg == {"action":"create_room"}

def test_receive_multiple_messages(network):
    sock = FakeSocket([b'{"a":1}\n{"b":2}\n'])
    msg = network.receive(sock)
    msg2 = network.receive(sock)
    msg3 = network.receive(sock)

    assert msg == {"a":1}
    assert msg2 == {"b":2}
    assert msg3 == None

def test_split_chunk(network):
    sock = FakeSocket([b'{"a":',b'1}\n'])

    msgs = []
    for i in range(2):
        msgs.append(network.receive(sock))

    assert msgs[0] == {"a":1}
    assert msgs[1] == None

def test_send(network):
    sock = FakeRecorderSocket()

    network.send(sock, {'action':'create_room'})
    payload = json.loads(sock.sent.decode())

    assert 'action' in payload
    assert payload['action'] == 'create_room'

    assert 'timestamp' in payload
    assert sock.sent.endswith(b"\n")
