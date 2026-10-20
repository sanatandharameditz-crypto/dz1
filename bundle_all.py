"""
DuelZone Bundler - Makes every game HTML file 100% self-contained
Embeds all external <script src="..."> files inline
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# Read a file, return content or empty string on error
def read_js(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ''

# All game HTML files (skip chess, ludo, tetris - they already embed their JS)
GAME_HTMLS = [
    'pong.html', 'pingpong.html', 'snake.html', 'airhockey.html',
    'tanks.html', 'bomberman.html', 'minesweeper.html', 'sudoku.html',
    'memory.html', 'connect4.html', 'game2048.html', 'battleship.html',
    'spacedodge.html', 'starcatcher.html', 'reaction.html', 'wordduel.html',
    'territory.html', 'darts.html', 'blackjack.html', 'pool.html',
    'checkers.html'
]

def bundle_html(filename):
    html_path = os.path.join(BASE, filename)
    if not os.path.exists(html_path):
        print(f"  SKIP (not found): {filename}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    def replace_script_src(m):
        src = m.group(1)
        # Build the full path to the JS file
        js_path = os.path.join(BASE, src.replace('/', os.sep))
        content = read_js(js_path)
        if content:
            print(f"    + Embedded: {src}")
            return f"<script>\n{content}\n</script>"
        else:
            print(f"    ! Missing:  {src}  (kept as external)")
            return m.group(0)

    # Replace all <script src="..."> tags (except http:// URLs)
    new_html = re.sub(
        r'<script\s+src=["\'](?!https?://)([^"\']+)["\']><\/script>',
        replace_script_src,
        html,
        flags=re.IGNORECASE
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"  OK: {filename}")

print("=== DuelZone Bundler ===")
for name in GAME_HTMLS:
    print(f"\nProcessing: {name}")
    bundle_html(name)

print("\n=== DONE! All game files are now self-contained ===")
