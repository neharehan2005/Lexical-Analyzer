# Lexical Analyzer

A DFA/state-machine-based lexical analyzer implemented in Python for a custom programming language.

The lexical analyzer reads source code from a `.txt` input file, scans it from left to right, identifies valid tokens, classifies them into their appropriate class parts, tracks line numbers, and reports lexical errors.

---

## Features

* Recognizes reserved keywords
* Recognizes identifiers beginning with `$`
* Recognizes integer and decimal numbers
* Recognizes text literals
* Recognizes truth literals
* Recognizes one-character operators
* Recognizes two-character operators
* Recognizes special characters
* Recognizes arrays
* Removes comments beginning with `#`
* Tracks source-code line numbers
* Reports invalid characters
* Reports invalid identifiers
* Reports unterminated text literals
* Uses DFA/state-machine logic for token recognition
* Uses a trie-based transition structure for reserved keywords
* Reads the complete source program from `source.txt`

---

# Project Structure

```text
Lexical-Analyzer/
│
├── lexer.py
├── source.txt
└── README.md
```

### Files

| File         | Purpose                                    |
| ------------ | ------------------------------------------ |
| `lexer.py`   | Contains the complete lexical analyzer     |
| `source.txt` | Contains the source program to be analyzed |
| `README.md`  | Project documentation                      |

---

# Input Source File

The lexer reads the source program from:

```text
source.txt
```

The source file should be placed in the **same folder** as `lexer.py`.

Example:

```text
Lexical-Analyzer/
│
├── lexer.py
└── source.txt
```

The source file can contain declarations, arrays, expressions, conditions, loops, tasks, function calls, comments, and other supported language constructs.

---

# Example Source Program

```text
begin
{
    declare $age1 as number set to 17
    declare $studentName2 as text set to "Sana"
    declare $isValid3 as truth set to true

    # this is a comment

    declare $marks1 as number set to 87
    declare $courseName2 as text set to "Compiler Construction"
    declare $passed4 as truth set to false

    declare $numbers1 as number array of 5
    declare $names2 as text array of 2 set to ["Sana", "Neha"]

    set $marks1 to $marks1 + 5

    show $studentName2
    show $marks1

    show "Student passed" if $marks1 >= 50
    otherwise
    show "Student failed"

    set $age1 to 18

    repeat while $age1 < 25
    {
        show $age1
        $age1++
    }

    task $calculate()
    {
        declare $total1 as number set to 100
        show "hello world"
        return
    }

    $calculate()

    ask $studentName2 with "Enter your name"
}
end
```

---

# How the Lexer Works

The lexer processes the source program from **left to right**.

For each character, it determines which type of token is starting.

The main function responsible for this is:

```python
tokenize()
```

It acts as the main dispatcher.

The basic decision process is:

```text
Character
    |
    ├── $       → scan_identifier()
    |
    ├── Digit   → scan_number()
    |
    ├── "       → scan_text()
    |
    ├── Letter  → scan_word()
    |
    └── Symbol  → scan_symbol()
```

The recognized token is then stored as a `Token` object.

---

# Token Structure

Each token contains three main pieces of information:

```text
LINE
LEXEME
CLASS PART
```

The `Token` class is defined as:

```python
class Token:
    __slots__ = ("lexeme", "class_part", "line")
```

Therefore, every token stores:

| Field        | Meaning                              |
| ------------ | ------------------------------------ |
| `lexeme`     | Actual text found in the source      |
| `class_part` | Classification assigned by the lexer |
| `line`       | Source-code line number              |

---

# Token Output

The lexer prints the tokens in the following format:

```text
LINE  LEXEME                      CLASS PART
----------------------------------------------------------------------
```

For example:

```text
2     'begin'                     begin
3     '{'                         {
4     'declare'                   declare
4     '$age1'                     Identifier
4     'as'                        as
4     'number'                    Data Type
4     'set'                       set
4     'to'                        to
4     '17'                        Number_literal
```

The **class-part names are exactly the values defined in `lexer.py`**.

---

# DFA / State-Machine Implementation

The project uses DFA and state-machine concepts in several parts of the lexical analyzer.

There are two major approaches:

1. A trie/transition structure for reserved keywords
2. State-machine functions for identifiers, numbers, text literals, and symbols

---

# Whitespace Handling

The lexical analyzer **ignores whitespace** between tokens.

Whitespace includes:

```text
spaces
tabs
```

For example, the following:

```text
declare    $age1    as    number
```

and:

```text
declare $age1 as number
```

produce the same tokens:

```text
declare       → declare
$age1         → Identifier
as            → as
number        → Data Type
```

Leading and trailing whitespace is removed during preprocessing using:

```python
line = line.strip()
```

During tokenization, whitespace characters are skipped using:

```python
if c.isspace():
    i += 1
    continue
```

Therefore, whitespace **does not become a token**. It only separates tokens.

For example:

```text
show      $age1
```

is tokenized as:

```text
show       → show
$age1      → Identifier
```

Extra spaces do not affect the lexical classification of the source code.


# Keyword Recognition Using Trie

Reserved keywords are stored in the `KEYWORDS` dictionary.

Examples include:

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

The lexer builds a trie from these keywords using:

```python
_build_trie()
```

The resulting structure is stored in:

```python
KEYWORD_TRIE
```

For example, the word:

```text
begin
```

can be viewed as transitions:

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

When the complete word matches a reserved keyword, its corresponding class part is returned.

For example:

```text
begin → begin
end   → end
if    → if
while → while
```

---

# Reserved Keywords

The lexer recognizes the following reserved keywords:

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

Each keyword uses its own name as the class part.

For example:

```text
begin      → begin
declare    → declare
set        → set
while      → while
otherwise  → otherwise
task       → task
return     → return
```

---

# Data Types

The language supports the following data types:

```text
number
text
truth
```

They are classified as:

```text
number → Data Type
text   → Data Type
truth  → Data Type
```

Example:

```text
declare $age1 as number
```

produces:

```text
declare       → declare
$age1         → Identifier
as            → as
number        → Data Type
```

---

# Truth Literals

The lexer recognizes:

```text
true
false
unknown
```

These are classified as:

```text
Truth_literal
```

For example:

```text
true  → Truth_literal
false → Truth_literal
```

---

# Identifier DFA

Identifiers in the language begin with:

```text
$
```

Examples:

```text
$age1
$studentName2
$isValid3
$marks1
$courseName2
```

The lexer uses:

```python
scan_identifier()
```

The general structure is:

```text
START
  |
  $
  ↓
Read letter
  |
  ↓
Read remaining letters/digits
  |
  ↓
ACCEPT
```

The lexer requires the character immediately after `$` to be a letter.

For example:

```text
$age1
```

is valid.

But:

```text
$123
```

is reported as an invalid identifier.

---

# Number DFA

Numbers are recognized by:

```python
scan_number()
```

The lexer supports integer and decimal numbers.

Examples:

```text
17
50
87
18
78.50
123.45
```

A simplified state structure is:

```text
START
  |
  digit
  ↓
DIGIT
  |
  ├── digit → DIGIT
  |
  └── . → DECIMAL
             |
             digit
             ↓
           DIGIT
             |
             ↓
           ACCEPT
```

Examples:

```text
17       → Number_literal
87       → Number_literal
78.50    → Number_literal
```

---

# Text Literal DFA

Text literals are enclosed in double quotes.

Example:

```text
"Sana"
```

The lexer uses:

```python
scan_text()
```

The basic state flow is:

```text
START
  |
  "
  ↓
TEXT
  |
  | characters
  ↓
TEXT
  |
  "
  ↓
ACCEPT
```

Examples:

```text
"Sana"
"Compiler Construction"
"hello world"
"Student passed"
```

are classified as:

```text
Text_literal
```

If the closing quote is missing, the lexer reports:

```text
ERROR: UNTERMINATED_TEXT_LITERAL
```

---

# Operators

Operators are handled by:

```python
scan_symbol()
```

The lexer first checks for two-character operators and then checks one-character operators.

This is important because an operator such as:

```text
>=
```

must be recognized as one token rather than:

```text
>
=
```

---

## Two-Character Operators

The lexer supports:

```text
++
--
<=
>=
&&
||
```

Their class parts are the operators themselves.

For example:

```text
>= → >=
++ → ++
```

---

## One-Character Operators

The lexer supports:

```text
+
-
*
/
%
<
>
!
=
```

Examples:

```text
+ → +
- → -
< → <
> → >
= → =
```

---

# Special Characters

Special characters are stored in:

```python
SPECIAL_CHARACTERS
```

The lexer supports:

```text
{
}
(
)
:
;
?
_
[
]
,
#
```

The class part of each special character is the character itself.

For example:

```text
{ → {
} → }
( → (
) → )
[ → [
] → ]
, → ,
```

---

# Arrays

The language supports array declarations.

Example:

```text
declare $numbers1 as number array of 5
```

The lexer recognizes:

```text
declare       → declare
$numbers1     → Identifier
as            → as
number        → Data Type
array         → array
of            → of
5             → Number_literal
```

Array values can also contain multiple elements.

Example:

```text
["Sana", "Neha"]
```

The lexer recognizes:

```text
[        → [
"Sana"   → Text_literal
,        → ,
"Neha"   → Text_literal
]        → ]
```

Similarly:

```text
[78, 98, 20]
```

produces:

```text
[        → [
78       → Number_literal
,        → ,
98       → Number_literal
,        → ,
20       → Number_literal
]        → ]
```

The lexer identifies the individual tokens. Validation of whether the array has the correct size or correct data type would normally be handled by later compiler phases.

---

# Comments

Comments begin with:

```text
#
```

Example:

```text
# this is a comment
```

Comments are removed during preprocessing.

The function responsible for this is:

```python
preprocess()
```

For example:

```text
declare $marks1 as number set to 87

# this is a comment

declare $courseName2 as text set to "Compiler Construction"
```

The comment does not generate tokens.

However, line numbers are preserved because the lexer processes the original lines before tokenization.

---

# Preprocessing

The function:

```python
preprocess()
```

performs basic preparation of the source code.

It:

1. Reads the source line by line.
2. Removes comments beginning with `#`.
3. Removes unnecessary leading and trailing whitespace.
4. Keeps the lines so that line numbers can be tracked.

---

# Main Functions

| Function            | Purpose                                             |
| ------------------- | --------------------------------------------------- |
| `_build_trie()`     | Builds the keyword transition structure             |
| `preprocess()`      | Removes comments and prepares source lines          |
| `scan_word()`       | Recognizes keywords, data types, and truth literals |
| `scan_identifier()` | Recognizes `$` identifiers                          |
| `scan_number()`     | Recognizes integer and decimal numbers              |
| `scan_text()`       | Recognizes text literals                            |
| `scan_symbol()`     | Recognizes operators and special characters         |
| `tokenize()`        | Main dispatcher that generates tokens               |
| `print_tokens()`    | Displays the generated token table                  |

---

# Complete Processing Flow

The complete lexer workflow is:

```text
                 source.txt
                     |
                     ↓
                Read Source
                     |
                     ↓
                preprocess()
                     |
                     ↓
                  tokenize()
                     |
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Letter      Digit        $
          |          |           |
          ↓          ↓           ↓
     scan_word   scan_number  scan_identifier
          |
          ↓
    Keyword Trie
          |
          ↓
     Token Object
          |
          ↓
       Token List
          |
          ↓
     print_tokens()
```

Symbols follow:

```text
Symbol
   |
   ↓
scan_symbol()
   |
   ├── Two-character operator
   |
   ├── One-character operator
   |
   └── Special character
```

---

# Error Handling

The lexer reports lexical errors when invalid input is encountered.

## Invalid Identifier

Example:

```text
$123
```

This is invalid because an identifier must begin with `$` followed by a letter.

The lexer can report:

```text
ERROR: INVALID_IDENTIFIER
```

---

## Undefined Word

If a normal alphabetic word is not present in the keyword table, the lexer reports:

```text
ERROR: UNDEFINED_WORD
```

This helps identify unsupported or misspelled keywords.

---

## Invalid Character

Characters that are not recognized as valid operators or special characters are reported as:

```text
ERROR: INVALID_CHARACTER
```

---

## Unterminated Text Literal

Example:

```text
"Hello World
```

Because the closing `"` is missing, the lexer reports:

```text
ERROR: UNTERMINATED_TEXT_LITERAL
```

---

# Source File and Lexer Separation

The source program is kept separate from the lexer implementation.

The lexer is stored in:

```text
lexer.py
```

while the program being analyzed is stored in:

```text
source.txt
```

Therefore, the source program does **not** need to be written directly inside `lexer.py`.

The lexer reads it using:

```python
with open(filename, "r", encoding="utf-8") as f:
    src = f.read()
```

By default, the filename is:

```text
source.txt
```

---

# How to Run

## Step 1 — Open PowerShell

Open PowerShell or Command Prompt.

Go to the project directory.

For example:

```powershell
cd "$HOME\Downloads\Lexical-Analyzer"
```

---

## Step 2 — Check Python

Run:

```powershell
py --version
```

You should see something similar to:

```text
Python 3.x.x
```

---

## Step 3 — Run the Lexer

Because `lexer.py` automatically uses `source.txt`, simply run:

```powershell
py lexer.py
```

The program will:

```text
lexer.py
   ↓
source.txt
   ↓
preprocess()
   ↓
tokenize()
   ↓
print_tokens()
```

---

# Running With Another Input File

The lexer also supports providing a different input filename through the command line.

For example:

```powershell
py lexer.py test_input.txt
```

In this case, the lexer reads:

```text
test_input.txt
```

instead of the default:

```text
source.txt
```

This makes it possible to test multiple source programs without changing `lexer.py`.

---

# Example Command

If the project contains:

```text
Lexical-Analyzer/
│
├── lexer.py
├── source.txt
└── test_input.txt
```

Run the default source:

```powershell
py lexer.py
```

Or run another source:

```powershell
py lexer.py test_input.txt
```

---

# Technologies Used

* Python 3
* Deterministic Finite Automata (DFA)
* State Machines
* Trie / Transition Structure
* Lexical Analysis
* Regular-Language Concepts
* Compiler Construction

---

# Learning Objectives

This project demonstrates:

1. How a lexical analyzer works.
2. How source code is divided into tokens.
3. How DFA concepts can be implemented in Python.
4. How transition structures can be used for keyword recognition.
5. How state-machine functions recognize identifiers.
6. How numbers and text literals are recognized.
7. How operators and special characters are classified.
8. How comments are removed during preprocessing.
9. How line numbers are maintained.
10. How lexical errors are detected.
11. How a lexer can read source code from an external `.txt` file.

---

# Compiler Workflow

The lexical analyzer represents the first major phase of compilation.

```text
Source Program
      |
      ↓
Lexical Analysis
      |
      ↓
Tokens
      |
      ↓
Syntax Analysis / Parser
      |
      ↓
Semantic Analysis
      |
      ↓
Intermediate Code
      |
      ↓
Code Generation
```

The current project focuses on the **lexical analysis phase**.

The lexer does not determine whether the complete program follows the grammar of the language. It only identifies and classifies individual tokens.

---

# Important Note

The lexer recognizes tokens such as:

```text
begin
{
declare
$age1
as
number
set
to
17
}
end
```

It does **not** determine whether these tokens occur in the correct grammatical order.

For example, determining whether:

```text
declare $age1 as number set to 17
```

is a valid statement is the responsibility of the **parser**, which is a later compiler phase.

Therefore:

```text
Lexer → "What token is this?"
Parser → "Is this sequence of tokens grammatically correct?"
```

---

# Author

Compiler Construction Project

University of Karachi — UBIT

BS Computer Science

---

# License

This project is intended for educational purposes.
