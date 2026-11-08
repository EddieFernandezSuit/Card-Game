from card_game.core.game_state import GameState


class RecordingClient:
    def __init__(self):
        self.processed = 0

    def process_messages(self):
        self.processed += 1


def test_state_without_client_processes_no_network_messages():
    # The menu and deck-builder states have no client, so the main update
    # loop must be able to call process_network without raising.
    state = GameState(object(), 'menu')

    state.process_network()


def test_state_with_client_processes_network_messages():
    state = GameState(object(), 'play')
    state.client = RecordingClient()

    state.process_network()

    assert state.client.processed == 1
