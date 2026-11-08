# Card-Game

A two-player online trading card game built with [pygame](https://www.pygame.org/).

## Open Game

Run `CardGame.exe`, or start the game with Python:

```bash
pip install -r requirements.txt
python main.py
# or: python -m card_game
```

To play online, start the server first and then launch two clients:

```bash
python run_server.py
python main.py
```

On Windows, `run.bat` starts the server and two clients automatically.

## Game Information

This game plays similarly to Hearthstone and other popular online trading card games.

- There are two players, each with their own hand.
- One hand is at the top of the screen and the other is at the bottom.
- Each player's mana and health are shown on the right of the screen.
- Each unit costs mana to play.
- Play units onto the battlefield and use them to fight your opponent's units and deal damage to your opponent's health.
- The first player to reduce their opponent's health to zero wins.

Make sure to edit your deck before playing. The deck editor is available from the main menu.

## Controls

- Click a card in your hand whose mana cost is affordable to play it.
- Click a card on the field to attack with it.
- Click the right arrow or press `Space` to pass your turn.

## Project Layout

```text
card_game/
  app.py              # Application bootstrap and frame update hook
  server.py           # Server entry point
  core/               # Game loop, state, paths, constants, shared helpers
  components/         # Reusable entity behaviours (click, image, stats, transform)
  entities/           # Cards, players, zones, text, and other game objects
  network/            # Client/server networking and session helpers
  states/             # Menu, lobby, deck-builder, and play screen builders
assets/               # Images and sounds
data/                 # Card definitions and saved decks
tests/                # Pytest suite
tools/                # One-off development utilities
main.py               # Client entry point
run_server.py         # Server entry point
```

The code under `card_game/` is the implementation. The root `main.py` and
`run_server.py` are thin entry points kept for convenience.

## Development

Python 3.12 is recommended.

```bash
pip install -e ".[dev]"
python -m pytest
flake8 .
```

The test suite runs headless by configuring SDL's dummy video and audio drivers
in `tests/conftest.py`.
