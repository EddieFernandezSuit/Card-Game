import main
from card_game.core.game_state import GameState


class FakeMusic:
    def __init__(self):
        self.stop_calls = 0

    def stop(self):
        self.stop_calls += 1


class FakeSocket:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class FakeClient:
    def __init__(self):
        self.client = FakeSocket()
        self.sent = []
        self.update_game_state = None

    def send(self, message):
        self.sent.append(message)


class FakePassTurnButton:
    def __init__(self):
        self.clicks = 0

    def on_click(self):
        self.clicks += 1


class FakeGame:
    def __init__(self):
        self.states = {'menu': 'menu-state', 'play': GameState(self, 'play')}
        self.currentState = self.states['play']
        self.set_state_calls = []

    def set_state(self, name):
        self.set_state_calls.append(name)
        self.currentState = self.states[name]


def test_leave_game_without_music_or_client_returns_to_menu():
    game = FakeGame()
    game.currentState = GameState(game, 'menu')

    main.on_click_leave_game(game)

    assert game.set_state_calls == ['menu']
    assert game.currentState == 'menu-state'


def test_leave_game_stops_music_and_disconnects_client():
    game = FakeGame()
    state = GameState(game, 'play')
    state.background_music = FakeMusic()
    state.client = FakeClient()
    game.currentState = state

    main.on_click_leave_game(game)

    assert state.background_music.stop_calls == 1
    assert state.client.sent == [{'leave_game': ''}]
    assert state.client.client.closed is True
    assert game.set_state_calls == ['menu']


def test_try_pass_turn_does_nothing_without_a_button():
    game = FakeGame()
    game.currentState = GameState(game, 'menu')

    main.try_pass_turn(game)


def test_try_pass_turn_clicks_the_button_when_present():
    game = FakeGame()
    button = FakePassTurnButton()
    game.currentState.passTurnButton = button

    main.try_pass_turn(game)

    assert button.clicks == 1
