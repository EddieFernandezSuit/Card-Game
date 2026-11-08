"""Server entry point."""

from card_game.network import Server


def main():
    Server(8000)


if __name__ == '__main__':
    main()
