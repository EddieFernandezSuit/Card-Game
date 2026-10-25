import re, os, sys

root = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\ferna\Downloads\Software\card-game'

# Only replace game.currentState.key and game.currentState.key
pattern1 = re.compile(r"game\.currentState\['([^']+)'\]")
pattern2 = re.compile(r'game\.currentState\["([^"]+)"\]')

for dirpath, dirnames, filenames in os.walk(root):
    if '__pycache__' in dirpath:
        continue
    for fn in filenames:
        if not fn.endswith('.py'):
            continue
        path = os.path.join(dirpath, fn)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue
        new_content = pattern1.sub(r'game.currentState.\1', content)
        new_content = pattern2.sub(r'game.currentState.\1', new_content)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print('updated', path)
