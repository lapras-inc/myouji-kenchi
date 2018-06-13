import unicodedata

CHARACTER_INVENTORY = [
    # Input
    *[chr(i) for i in range(ord('a'), ord('z') + 1)],
    *[chr(i) for i in range(ord('A'), ord('Z') + 1)],
    unicodedata.lookup('COMBINING MACRON'),
    unicodedata.lookup('COMBINING CIRCUMFLEX ACCENT'),
    '\'',
    '-',
    '$',
    # Output
    *[chr(i) for i in range(ord('ァ'), ord('ヺ') + 1)]
]

EPSILON = 'ε'
SYMBOL_TABLE = {EPSILON: 0}

for c in CHARACTER_INVENTORY:
    SYMBOL_TABLE[c] = len(SYMBOL_TABLE)

REVERSE_SYMBOL_TABLE = {v: k for k, v in SYMBOL_TABLE.items()}
