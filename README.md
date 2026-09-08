# Lexical Analyzer

A DFA-based lexical analyzer implemented in Python for a custom programming language.

The lexical analyzer reads source code, identifies valid tokens, classifies them, and reports lexical errors.

---

## Features

* Recognizes reserved keywords
* Recognizes identifiers
* Recognizes numbers
* Recognizes text literals
* Recognizes truth literals
* Recognizes operators
* Recognizes special characters
* Removes comments beginning with `#`
* Tracks line numbers
* Reports invalid characters and malformed tokens
* Uses DFA/state-machine logic for lexical recognition
* Uses a transition table/trie for reserved keywords

---

## Project Structure

```text
Lexical-Analyzer/
│
├── lexer.py
├── README.md

```

### Main File

`lexer.py`

This file contains the complete lexical analyzer.

---

# How the Lexer Works

The lexer processes the source code from left to right.

For every character, it determines what type of token is starting.

The main function responsible for this is:

```python
tokenize()
```

It acts as the **dispatcher**.

For example:

```text
Letter       → scan_word()
$            → scan_identifier()
Digit        → scan_number()
"            → scan_text()
Operator     → scan_symbol()
Special char → scan_symbol()
```

---

# DFA Implementation

The project uses DFA/state-machine concepts in two ways.

## 1. Transition Table for Keywords

Reserved keywords such as:

```text
begin
end
declare
set
while
if
otherwise
repeat
show
ask
```

are recognized using a **transition table implemented as a trie**.

For example, for:

```text
begin
```

the lexer follows transitions similar to:

```text
START
  |
  b
  ↓
  e
  ↓
  g
  ↓
  i
  ↓
  n
  ↓
ACCEPT
```

The characters are processed one by one.

The keyword transition structure is stored in:

```python
KEYWORD_TRIE
```

The lexer checks whether the complete word reaches an accepting state.

For example:

```text
begin
```

is recognized as the reserved keyword:

```text
Class: begin
Part : BEGIN
```

---

# 2. DFA Through Functions

Other token types are implemented using state-machine logic inside functions.

The important functions are:

```python
scan_identifier()
scan_number()
scan_text()
scan_symbol()
```

These functions represent the transitions between states.

---

## Identifier DFA

Identifiers in this language start with:

```text
$
```

For example:

```text
$age
$total
$name1
```

The process is approximately:

```text
START
  |
  $
  ↓
IDENTIFIER
  |
  letter/digit/underscore
  ↓
IDENTIFIER
  |
  invalid character
  ↓
ACCEPT
```

The function responsible for this is:

```python
scan_identifier()
```

---

# Number DFA

Numbers are recognized by:

```python
scan_number()
```

For example:

```text
123
45
78.50
```

The state machine reads digits and, when applicable, the decimal point and following digits.

Example:

```text
123.45
```

```text
START
  |
  1
  ↓
DIGIT
  |
  2
  ↓
DIGIT
  |
  3
  ↓
DIGIT
  |
  .
  ↓
DECIMAL
  |
  4
  ↓
DIGIT
  |
  5
  ↓
ACCEPT
```

---

# Text Literal DFA

Text values are enclosed in double quotes.

Example:

```text
"Hello"
```

The lexer uses:

```python
scan_text()
```

The basic process is:

```text
START
  |
  "
  ↓
TEXT
  |
  characters
  ↓
TEXT
  |
  "
  ↓
ACCEPT
```

Example:

```text
"Hello World"
```

is recognized as a text literal.

---

# Operators

Operators are handled by:

```python
scan_symbol()
```

Examples include:

```text
+
-
*
/
=
==
!=
<
>
<=
>=
```

Operators are returned with the token class:

```text
OP
```

Example:

```text
+
```

produces:

```text
Class: OP
Part : +
```

---

# Special Characters

Special characters are structural characters used by the language.

They are classified as:

```text
SPCL
```

`SPCL` means:

> Special Character

Examples:

| Character | Class | Part       |
| --------- | ----- | ---------- |
| `{`       | SPCL  | LBRACE     |
| `}`       | SPCL  | RBRACE     |
| `(`       | SPCL  | LPAREN     |
| `)`       | SPCL  | RPAREN     |
| `[`       | SPCL  | LBRACKET   |
| `]`       | SPCL  | RBRACKET   |
| `:`       | SPCL  | COLON      |
| `;`       | SPCL  | SEMICOLON  |
| `,`       | SPCL  | COMMA      |
| `?`       | SPCL  | QMARK      |
| `_`       | SPCL  | UNDERSCORE |

For example:

```text
[78, 98, 20]
```

will contain:

```text
[    → SPCL / LBRACKET
78   → NUMBER
,    → SPCL / COMMA
98   → NUMBER
,    → SPCL / COMMA
20   → NUMBER
]    → SPCL / RBRACKET
```

---

# Reserved Keywords

Reserved keywords are recognized separately from normal identifiers.

Examples:

```text
begin
end
declare
as
set
to
array
of
show
ask
with
repeat
while
if
otherwise
task
return
at
```

The class of each reserved keyword is its own name.

For example:

```text
begin → class = begin
end   → class = end
if    → class = if
while → class = while
```

Data types remain separate:

```text
number → DT
text   → DT
truth  → DT
```

Truth literals are:

```text
true    → Truth_literal
false   → Truth_literal
unknown → Truth_literal
```

---

# Token Structure

Each token contains:

```text
Lexeme
Class
Part
Line
```

For example:

```text
begin
```

may produce:

```text
Lexeme : begin
Class  : begin
Part   : BEGIN
Line   : 1
```

For a number:

```text
123
```

the result is approximately:

```text
Lexeme : 123
Class  : NUMBER
Part   : INTEGER
Line   : 1
```

---

# Comments

Comments begin with:

```text
#
```

Example:

```text
begin

# this is a comment

declare $age as number
```

The comment is removed during preprocessing.

The function responsible for this is:

```python
preprocess()
```

---

# Complete Processing Flow

The complete lexer flow is:

```text
                Source Code
                     |
                     ↓
                preprocess()
                     |
                     ↓
                  tokenize()
                     |
          ┌──────────┼──────────┐
          ↓          ↓          ↓
      Letter       Digit        $
          |          |           |
          ↓          ↓           ↓
     scan_word   scan_number  scan_identifier
          |
          ↓
   Keyword Transition
       Table / Trie
          |
          ↓
       Token List
          |
          ↓
      print_tokens()
```

Symbols follow another path:

```text
Symbol
  |
  ↓
scan_symbol()
  |
  ├── Operator → OP
  |
  └── Special Character → SPCL
```

---

# Why Both Transition Tables and Functions?

The project uses both because different token types are easier to represent differently.

### Keywords

Keywords have many possible character paths, so a transition table/trie is used.

```text
b → e → g → i → n
```

### Identifiers

Identifiers follow a simple pattern, so a function can implement their states.

```text
$ → letters/digits/underscore
```

### Numbers

Numbers also have a simple state structure.

```text
digit → digit → ... → decimal → digit
```

### Text

Text follows:

```text
" → characters → "
```

### Symbols

Symbols can be checked directly against operator and special-character tables.

Therefore:

> **The project is DFA-based, but the DFA is implemented using both transition tables and state-machine functions.**

---

# How to Run

## Step 1 — Open PowerShell

Open PowerShell or Command Prompt.

Go to the folder containing `lexer.py`.

For example:

```powershell
cd $HOME\Downloads
```

If your project is inside another folder:

```powershell
cd "$HOME\Downloads\Lexical-Analyzer"
```

---

## Step 2 — Check Python

Run:

```powershell
py --version
```

If Python is installed, you should see something similar to:

```text
Python 3.x.x
```

---

## Step 3 — Run the Lexer

Run:

```powershell
py lexer.py
```

Python officially supports running a script by supplying its filename to the interpreter.

If the `python` command works on your computer, you can also use:

```powershell
python lexer.py
```

---

# Running With an Input File

If the lexer supports a filename argument, create:

```text
test_input.txt
```

For example:

```text
begin

declare $age as number

set $age to 20

show with $age

end
```

Then run:

```powershell
py lexer.py test_input.txt
```

The lexer will read the source file and generate tokens.

---

# Example Input

```text
begin

declare $age as number

set $age to 20

if $age >= 18 {
    show with "Adult"
}

otherwise {
    show with "Minor"
}

end
```

---

# Example Token Output

The exact formatting depends on `print_tokens()`, but conceptually the output will look like:

```text
Lexeme      Class             Part
------------------------------------------------
begin       begin             BEGIN
declare     declare           DECLARE
$age        ID                IDENTIFIER
as          as                AS
number      DT                NUMBER
set         set               SET
$age        ID                IDENTIFIER
to          to                TO
20          NUMBER            INTEGER
if          if                IF
$age        ID                IDENTIFIER
>=          OP                >=
18          NUMBER            INTEGER
{           SPCL              LBRACE
show        show              SHOW
with        with              WITH
"Adult"     TEXT              TEXT
}           SPCL              RBRACE
end         end               END
```

---

# Error Handling

The lexer reports invalid input instead of silently accepting it.

Examples of possible errors include:

```text
INVALID_CHARACTER
UNTERMINATED_TEXT
INVALID_NUMBER
INVALID_IDENTIFIER
```

Errors can be displayed using:

```python
print_errors()
```

---

# Main Functions

| Function            | Purpose                                       |
| ------------------- | --------------------------------------------- |
| `preprocess()`      | Removes comments and prepares input           |
| `tokenize()`        | Main dispatcher                               |
| `scan_word()`       | Recognizes keywords/data types/truth literals |
| `scan_identifier()` | Recognizes identifiers                        |
| `scan_number()`     | Recognizes numbers                            |
| `scan_text()`       | Recognizes text literals                      |
| `scan_symbol()`     | Recognizes operators/special characters       |
| `print_tokens()`    | Displays generated tokens                     |
| `print_errors()`    | Displays lexical errors                       |

---

# Technologies Used

* Python 3
* Deterministic Finite Automata (DFA)
* Transition Tables
* Trie
* State Machines
* Lexical Analysis
* Regular-Language Concepts

---

# Learning Objectives

This project demonstrates:

1. How a lexical analyzer works.
2. How source code is divided into tokens.
3. How DFA concepts can be implemented in Python.
4. How transition tables represent DFA transitions.
5. How functions can implement state-machine behavior.
6. How keywords are distinguished from identifiers.
7. How operators and special characters are classified.
8. How lexical errors are detected.

---

# Project Workflow

```text
Source Program
      ↓
Preprocessing
      ↓
Character Reading
      ↓
Token Recognition
      ↓
DFA / State Transitions
      ↓
Token Classification
      ↓
Token List
      ↓
Error Reporting
```

---

# Requirements

No external Python packages are required if `lexer.py` only uses Python's standard library.

You only need:

```text
Python 3
```

---

# Author

**Neha Rehan**

Compiler Construction Project

University of Karachi — UBIT

BS Computer Science

---

# License

This project is intended for educational purposes.
