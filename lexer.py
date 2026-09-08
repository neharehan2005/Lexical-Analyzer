"""
================================================================================
 LEXICAL ANALYZER
 Built from: DFA_.pdf (hand-drawn DFA) + Language_Specification_Final.pdf
 Course: Compiler Construction - Section B
================================================================================

WHAT THIS FILE DOES
--------------------
1. Reads the source program character by character (no regex-based
   tokenizing -- every token is recognized by walking an explicit
   finite-automaton, exactly like the hand-drawn DFA).
2. Strips whitespace and single-line `#` comments, line by line
   (using str.strip(), as requested), before scanning begins.
3. Implements the DFA in two complementary ways, as requested:
      (a) TRANSITION TABLE  -> the keyword recognizer is a literal
          nested-dictionary transition table (a trie).
      (b) FUNCTIONS         -> identifiers, number literals, text
          literals and operators/special characters are each
          recognized by a dedicated state-machine function.
4. Completes the DFA where the drawing was incomplete:
      - Adds the `end` reserved keyword.
      - Makes the implicit "DEAD state" concrete.
================================================================================
"""

import sys


# ============================================================================
# 1. TOKEN OBJECT
# ============================================================================

class Token:
    __slots__ = ("lexeme", "tclass", "part", "line")

    def __init__(self, lexeme, tclass, part, line):
        self.lexeme = lexeme
        self.tclass = tclass
        self.part = part
        self.line = line

    def __repr__(self):
        return f"<{self.line:>3} | {self.lexeme!r:<20} | {self.tclass:<14} | {self.part}>"


# ============================================================================
# 2. KEYWORD TRANSITION TABLE
# ============================================================================

# For reserved keywords:
# CLASS = keyword name
# PART  = keyword name in uppercase
#
# Example:
# begin -> CLASS: begin, PART: BEGIN
# declare -> CLASS: declare, PART: DECLARE

KEYWORDS = {
    # --- Reserved Keywords ---
    "begin":     ("begin", "BEGIN"),
    "end":       ("end", "END"),
    "declare":   ("declare", "DECLARE"),
    "as":        ("as", "AS"),
    "set":       ("set", "SET"),
    "to":        ("to", "TO"),
    "array":     ("array", "ARRAY"),
    "of":        ("of", "OF"),
    "show":      ("show", "SHOW"),
    "ask":       ("ask", "ASK"),
    "with":      ("with", "WITH"),
    "repeat":    ("repeat", "REPEAT"),
    "while":     ("while", "WHILE"),
    "if":        ("if", "IF"),
    "otherwise": ("otherwise", "OTHERWISE"),
    "task":      ("task", "TASK"),
    "return":    ("return", "RETURN"),
    "at":        ("at", "AT"),

    # --- Data Types ---
    "number":    ("DT", "NUMBER"),
    "text":      ("DT", "TEXT"),
    "truth":     ("DT", "TRUTH"),

    # --- Truth Literals ---
    "true":      ("Truth_literal", "TRUE"),
    "false":     ("Truth_literal", "FALSE"),
    "unknown":   ("Truth_literal", "UNKNOWN"),
}


def _build_trie(words):
    """
    Build the nested-dictionary transition table (trie/DFA).

    Each node represents a DFA state.
    '$' represents an accepting state.
    """
    root = {}

    for word, value in words.items():
        node = root

        for ch in word:
            node = node.setdefault(ch, {})

        node["$"] = value

    return root


KEYWORD_TRIE = _build_trie(KEYWORDS)


# ============================================================================
# 3. OPERATOR / SPECIAL-CHARACTER TRANSITION TABLE
# ============================================================================

TWO_CHAR_OPERATORS = {
    "++": "IO",
    "--": "DO",
    "<=": "LE",
    ">=": "GE",
    "&&": "AND",
    "||": "OR",
}

ONE_CHAR_OPERATORS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MUL",
    "/": "DIV",
    "%": "MOD",
    "<": "LT",
    ">": "GT",
    "!": "NOT",
    "=": "ASSIGN",
}

SPECIAL_CHARACTERS = {
    "{": "LBRACE",
    "}": "RBRACE",
    "(": "LPAREN",
    ")": "RPAREN",
    ":": "COLON",
    ";": "SEMICOLON",
    "?": "QMARK",
    "_": "UNDERSCORE",
    "[": "LBRACKET",
    "]": "RBRACKET",
    ",": "COMMA",
}


# ============================================================================
# 4. PREPROCESSING
# ============================================================================

def preprocess(source_text):
    """
    Removes # comments and surrounding whitespace from every line.
    Blank lines are preserved so line numbers remain correct.
    """
    cleaned_lines = []

    for raw_line in source_text.splitlines():
        line = raw_line.rstrip("\n")

        if "#" in line:
            line = line[:line.index("#")]

        line = line.strip()
        cleaned_lines.append(line)

    return cleaned_lines


# ============================================================================
# 5. STATE-MACHINE FUNCTIONS
# ============================================================================

def scan_word(line, i):
    """
    Walk through the keyword transition table character by character.

    If the complete word is found in KEYWORDS, return its class and part.
    Otherwise, return ERROR.
    """

    start = i
    node = KEYWORD_TRIE
    n = len(line)

    # Walk through DFA transition states
    while i < n and line[i].isalpha() and line[i] in node:
        node = node[line[i]]
        i += 1

    # Consume remaining word characters
    while i < n and (line[i].isalnum() or line[i] == "_"):
        i += 1

    lexeme = line[start:i]

    value = KEYWORDS.get(lexeme)

    if value is not None:
        return (lexeme, value[0], value[1]), i

    # DEAD state
    return (
        lexeme,
        "ERROR",
        "UNDEFINED_WORD "
        "(bare words must be a keyword; variables must start with '$')"
    ), i


def scan_identifier(line, i):
    """
    Identifier DFA:

        S0 --'$'--> S1
        S1 --letter--> S2
        S2 --letter/digit--> S2
        S2 --digit--> S3
        S3 = ACCEPTING

    Identifier must start with $ and end with a digit.
    """

    start = i
    n = len(line)

    i += 1
    state = "S1"

    # Must have a letter after $
    if i >= n or not line[i].isalpha():
        lexeme = line[start:i]

        return (
            lexeme,
            "ERROR",
            "INVALID_IDENTIFIER (must start with $letter)"
        ), i

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
        return (
            lexeme,
            "ID",
            "IDENTIFIER"
        ), i

    return (
        lexeme,
        "ERROR",
        "INVALID_IDENTIFIER (must end with a digit)"
    ), i


def scan_number(line, i):
    """
    Number literal DFA:

        S0 --digit--> S1
        S1 --digit--> S1
        S1 --'.'--> S2
        S2 --digit--> S3
        S3 --digit--> S3

    Sign (+/-) is handled separately as an operator.
    """

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

    return (
        lexeme,
        "NUMBER_LITERAL",
        "NUMBER_LITERAL"
    ), i


def scan_text(line, i):
    """
    Text literal DFA:

        '"' --> characters --> '"'

    Missing closing quote = DEAD state.
    """

    start = i
    n = len(line)

    i += 1

    while i < n and line[i] != '"':
        i += 1

    if i < n and line[i] == '"':
        i += 1

        lexeme = line[start:i]

        return (
            lexeme,
            "TEXT_LITERAL",
            "TEXT_LITERAL"
        ), i

    lexeme = line[start:i]

    return (
        lexeme,
        "ERROR",
        "UNTERMINATED_TEXT_LITERAL"
    ), i


def scan_symbol(line, i):
    """
    Operator / special-character DFA.

    First checks two-character operators.
    Then one-character operators.
    Then special characters.

    This follows maximal munch.
    """

    # Check two-character operators first
    two = line[i:i + 2]

    if two in TWO_CHAR_OPERATORS:
        return (
            two,
            "OP",
            TWO_CHAR_OPERATORS[two]
        ), i + 2

    # Check one-character operators
    c = line[i]

    if c in ONE_CHAR_OPERATORS:
        return (
            c,
            "OP",
            ONE_CHAR_OPERATORS[c]
        ), i + 1

    # Check special characters
    if c in SPECIAL_CHARACTERS:
        return (
            c,
            "SPCL",
            SPECIAL_CHARACTERS[c]
        ), i + 1

    # DEAD state
    return (
        c,
        "ERROR",
        "INVALID_CHARACTER"
    ), i + 1


# ============================================================================
# 6. DRIVER
# ============================================================================

def tokenize(source_text):
    """
    Main lexer driver.

    Reads the source character by character and chooses
    the correct DFA/state-machine based on the first character.
    """

    tokens = []

    lines = preprocess(source_text)

    for line_no, line in enumerate(lines, start=1):

        i = 0
        n = len(line)

        while i < n:

            c = line[i]

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

            # Keyword / data type / truth literal
            elif c.isalpha():
                tok, i = scan_word(line, i)

            # Operators / special characters
            else:
                tok, i = scan_symbol(line, i)

            tokens.append(
                Token(
                    tok[0],
                    tok[1],
                    tok[2],
                    line_no
                )
            )

    return tokens


# ============================================================================
# 7. PRINT TOKENS
# ============================================================================

def print_tokens(tokens):

    header = (
        f"{'LINE':<6}"
        f"{'LEXEME':<24}"
        f"{'CLASS':<16}"
        f"{'PART'}"
    )

    print(header)
    print("-" * len(header))

    for t in tokens:

        print(
            f"{t.line:<6}"
            f"{t.lexeme!r:<24}"
            f"{t.tclass:<16}"
            f"{t.part}"
        )


# ============================================================================
# 8. PRINT ERRORS
# ============================================================================

def print_errors(tokens):

    errors = [
        t for t in tokens
        if t.tclass == "ERROR"
    ]

    print()
    print(
        f"{len(errors)} lexical error(s) found (DEAD state):"
    )

    print("-" * 60)

    for t in errors:

        print(
            f"  Line {t.line}: "
            f"invalid lexeme {t.lexeme!r} -> {t.part}"
        )

    if not errors:
        print("  (none)")


# ============================================================================
# 9. RUN
# ============================================================================

if __name__ == "__main__":

    if len(sys.argv) > 1:

        with open(
            sys.argv[1],
            "r",
            encoding="utf-8"
        ) as f:

            src = f.read()

    else:

        src = '''
begin
{
    # sample program exercising every token category

    declare $age1 as number set to 17

    declare $name7 as text set to "Sana"

    declare $isValid3 as truth set to unknown

    declare $num1 as number array of 3 set to [78, 98, 20]

    show $num1 at 1

    declare $i1 as number set to 0

    repeat while $i1 < 10
    {
        show $i1
        $i1++
    }

    show "Pass" if $age1 >= 18

    otherwise

    show "fail"

    task $helloWorld2()
    {
        show "Hello World"
        return
    }

    $helloWorld2()
}

end
'''

    all_tokens = tokenize(src)

    print_tokens(all_tokens)

    print_errors(all_tokens)

