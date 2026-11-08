"""Rewrite legacy ``game.currentState['key']`` access to attribute access.

This is a one-off migration helper; it is not imported by the game.
"""

import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]

# Only replace game.currentState.key and game.currentState.key
PATTERNS = [
    re.compile(r"game\.currentState\['([^']+)'\]"),
    re.compile(r'game\.currentState\["([^"]+)"\]'),
]


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT

    for path in root.rglob('*.py'):
        if '__pycache__' in path.parts:
            continue

        try:
            content = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue

        new_content = content
        for pattern in PATTERNS:
            new_content = pattern.sub(r'game.currentState.\1', new_content)

        if new_content != content:
            path.write_text(new_content, encoding='utf-8')
            print('updated', path)


if __name__ == '__main__':
    main()
