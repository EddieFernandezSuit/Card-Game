import socket
import threading
import pickle
import struct
import time


def recv_exact(sock: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("peer closed")
        buf.extend(chunk)
    return bytes(buf)


def run_once(payload_obj) -> None:
    parent_sock, child_sock = socket.socketpair()

    def sender():
        payload = pickle.dumps(payload_obj)
        header = struct.pack('!I', len(payload))

        # Send header in two parts, payload in multiple parts (simulates TCP fragmentation)
        parent_sock.sendall(header[:2])
        time.sleep(0.01)
        parent_sock.sendall(header[2:])

        # Fragment payload
        for i in range(0, len(payload), 7):
            parent_sock.sendall(payload[i:i+7])
            time.sleep(0.001)
        parent_sock.close()

    t = threading.Thread(target=sender, daemon=True)
    t.start()

    header = recv_exact(child_sock, 4)
    (length,) = struct.unpack('!I', header)
    payload = recv_exact(child_sock, length)
    obj = pickle.loads(payload)

    assert obj == payload_obj, f"Round-trip mismatch: {obj} != {payload_obj}"
    child_sock.close()
    t.join(timeout=1)


def main():
    run_once({"hello": "world"})
    run_once({"numbers": list(range(50))})
    run_once({"nested": {"a": [1, 2, 3], "b": "x"}, "t": time.time()})
    print("network framing test: PASS")


if __name__ == "__main__":
    main()

