
"""
================================================================================
 LEXICAL ANALYZER
 Course: Compiler Construction - Section B
================================================================================
"""

import sys


# ============================================================================
# 1. TOKEN OBJECT
# ============================================================================

class Token:
    __slots__ = ("lexeme", "class_part", "line")

    def __init__(self, lexeme, class_part, line):
        self.lexeme = lexeme
        self.class_part = class_part
        self.line = line

    def __repr__(self):
        return f"<{self.line:>3} | {self.lexeme!r:<24} | {self.class_part}>"


# ============================================================================
# 2. KEYWORD MAPPINGS & TRIE
# ============================================================================

# lexeme -> class_part
KEYWORDS = {

    # --- Reserved Keywords ---
    "begin":     "begin",
    "end":       "end",
    "declare":   "declare",
    "as":        "as",
    "set":       "set",
    "to":        "to",
    "array":     "array",
    "of":        "of",
    "show":      "show",
    "ask":       "ask",
    "with":      "with",
    "repeat":    "repeat",
    "while":     "while",
    "if":        "if",
    "otherwise": "otherwise",
    "task":      "task",
    "return":    "return",
    "at":        "at",

    # --- Data Types ---
    "number":    "Data Type",
    "text":      "Data Type",
    "truth":     "Data Type",

    # --- Truth Literals ---
    "true":      "Truth_literal",
    "false":     "Truth_literal",
    "unknown":   "Truth_literal",
}


def _build_trie(words):
    root = {}

    for word, value in words.items():
        node = root

        for ch in word:
            node = node.setdefault(ch, {})

        node["$"] = value

    return root


KEYWORD_TRIE = _build_trie(KEYWORDS)


# ============================================================================
# 3. OPERATORS & SPECIAL CHARACTERS
# ============================================================================

TWO_CHAR_OPERATORS = {
    "++": "++",
    "--": "--",
    "<=": "<=",
    ">=": ">=",
    "&&": "&&",
    "||": "||",
}


ONE_CHAR_OPERATORS = {
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "%": "%",
    "<": "<",
    ">": ">",
    "!": "!",
    "=": "=",
}


SPECIAL_CHARACTERS = {
    "{": "{",
    "}": "}",
    "(": "(",
    ")": ")",
    ":": ":",
    ";": ";",
    "?": "?",
    "_": "_",
    "[": "[",
    "]": "]",
    ",": ",",
    "#": "#",
}


# ============================================================================
# 4. PREPROCESSING
# ============================================================================

def preprocess(source_text):

    cleaned_lines = []

    for raw_line in source_text.splitlines():

        line = raw_line.rstrip("\n")

        # Remove comments
        if "#" in line:
            line = line[:line.index("#")]

        line = line.strip()

        cleaned_lines.append(line)

    return cleaned_lines


# ============================================================================
# 5. STATE-MACHINE FUNCTIONS
# ============================================================================

def scan_word(line, i):

    start = i
    node = KEYWORD_TRIE
    n = len(line)

    while i < n and line[i].isalpha() and line[i] in node:
        node = node[line[i]]
        i += 1

    while i < n and (line[i].isalnum() or line[i] == "_"):
        i += 1

    lexeme = line[start:i]

    value = KEYWORDS.get(lexeme)

    if value is not None:
        return (lexeme, value), i

    return (lexeme, "ERROR: UNDEFINED_WORD"), i


def scan_identifier(line, i):

    start = i
    n = len(line)

    i += 1  # consume '$'

    if i >= n or not line[i].isalpha():
        lexeme = line[start:i]
        return (lexeme, "ERROR: INVALID_IDENTIFIER"), i

    i += 1

    state = "S2"

    while i < n and (line[i].isalpha() or line[i].isdigit()):

        if line[i].isdigit():
            state = "S3"
        else:
            state = "S2"

        i += 1

    lexeme = line[start:i]

    if state == "S3":
        return (lexeme, "Identifier"), i

    return (lexeme, "ERROR: INVALID_IDENTIFIER"), i


def scan_number(line, i):

    start = i
    n = len(line)

    while i < n and line[i].isdigit():
        i += 1

    if (
        i < n
        and line[i] == "."
        and i + 1 < n
        and line[i + 1].isdigit()
    ):
        i += 1

        while i < n and line[i].isdigit():
            i += 1

    lexeme = line[start:i]

    return (lexeme, "Number_literal"), i


def scan_text(line, i):

    start = i
    n = len(line)

    i += 1  # consume opening quote

    while i < n and line[i] != '"':
        i += 1

    if i < n and line[i] == '"':

        i += 1

        lexeme = line[start:i]

        return (lexeme, "Text_literal"), i

    lexeme = line[start:i]

    return (
        lexeme,
        "ERROR: UNTERMINATED_TEXT_LITERAL"
    ), i


def scan_symbol(line, i):

    two = line[i:i + 2]

    # Check two-character operators first
    if two in TWO_CHAR_OPERATORS:
        return (two, TWO_CHAR_OPERATORS[two]), i + 2

    c = line[i]

    # Check one-character operators
    if c in ONE_CHAR_OPERATORS:
        return (c, ONE_CHAR_OPERATORS[c]), i + 1

    # Check special characters
    if c in SPECIAL_CHARACTERS:
        return (c, SPECIAL_CHARACTERS[c]), i + 1

    return (c, "ERROR: INVALID_CHARACTER"), i + 1


# ============================================================================
# 6. DRIVER
# ============================================================================

def tokenize(source_text):

    tokens = []

    lines = preprocess(source_text)

    for line_no, line in enumerate(lines, start=1):

        i = 0
        n = len(line)

        while i < n:

            c = line[i]

            # Ignore spaces
            if c.isspace():
                i += 1
                continue

            # Identifier
            if c == "$":
                tok, i = scan_identifier(line, i)

            # Number
            elif c.isdigit():
                tok, i = scan_number(line, i)

            # Text literal
            elif c == '"':
                tok, i = scan_text(line, i)

            # Keyword / word
            elif c.isalpha():
                tok, i = scan_word(line, i)

            # Operator / special character
            else:
                tok, i = scan_symbol(line, i)

            tokens.append(
                Token(tok[0], tok[1], line_no)
            )

    return tokens


# ============================================================================
# 7. PRINTING
# ============================================================================

def print_tokens(tokens):

    header = f"{'LINE':<6}{'LEXEME':<28}{'CLASS PART'}"

    print(header)
    print("-" * 70)

    for t in tokens:

        print(
            f"{t.line:<6}"
            f"{t.lexeme!r:<28}"
            f"{t.class_part}"
        )


# ============================================================================
# 8. RUN
# ============================================================================

if __name__ == "__main__":

    if len(sys.argv) > 1:
        # If a filename is provided:
        # py lexer.py source.txt
        filename = sys.argv[1]
    else:
        # Automatically use source.txt
        filename = "src.txt"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            src = f.read()

    except FileNotFoundError:
        print(f"ERROR: Source file '{filename}' not found.")
        print("Make sure the .txt file is in the same folder as lexer.py.")
        sys.exit(1)

    all_tokens = tokenize(src)

    print_tokens(all_tokens)

