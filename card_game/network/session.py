"""Client session teardown helpers."""


def disconnect_client(client):
    """Close a client connection without letting socket errors escape."""
    # The opponent leaving at the same time can close this socket from the
    # receive thread mid-teardown, so tolerate socket failures here.
    try:
        if client:
            client.update_game_state = lambda _: None
            client.send({'leave_game': ''})
            client.client.close()
    except OSError:
        pass
