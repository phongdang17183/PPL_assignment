# PPL Assignment (MiniGo)

This repository contains my coursework for the **Principles of Programming Languages (PPL)** class.  
The project follows a typical language front-end pipeline: **grammar definition -> lexer -> parser -> testing** -> **AST generation** and **static semantic checking**.

## Goals

- Practice designing a small language based on a given specification (MiniGo)
- Implement lexical rules (tokenization)
- Implement syntax rules (parsing)
- Implement AST generation 
- Implement Static checking
- Validate behavior using automated test suites

## What’s included

- **Specifications**
  - `Assignment 1 Spec.pdf`
  - `Assignment 2 Spec.pdf`
  - `Assignment3.pdf`
  - `MiniGo Spec 1.0.2.pdf`
- **Implementation**
  - `src/` (language implementation and related code)
- **Notes / template docs**
  - `README.txt`
  - `version 1.2.txt`

## Project workflow

The repo is structured to support incremental development:

1. Write / adjust grammar rules
2. Generate lexer & parser code from the grammar
3. Run test suites to verify lexer/parsing output
4. Extend to AST generation and semantic checking (optional / later phases)

## How to run

The assignment template provides a `run.py` script.  
Important: you must run commands **from the folder that contains `run.py`** (check `README.txt` to locate the correct working directory).

### Generate code

    python run.py gen

### Run tests

    python run.py test LexerSuite
    python run.py test ParserSuite
    python run.py test ASTGenSuite
    python run.py test CheckSuite

If a suite is not available in your current phase/template, simply skip it.

## Test suites (quick description)

- `LexerSuite`: checks tokenization (keywords, identifiers, literals, operators, comments, errors)
- `ParserSuite`: checks grammar structure (valid/invalid programs, declarations, statements, expressions)
- `ASTGenSuite`: checks AST building rules (if included in your phase)
- `CheckSuite`: checks static semantics such as scoping/types (if included in your phase)

## Common troubleshooting

- Command not found / files missing: run from the directory that contains `run.py`
- Grammar changes not reflected: re-run `python run.py gen` before testing
- Tests failing unexpectedly: compare outputs against the spec PDFs and update rules accordingly

## Author

Phong Dang  
GitHub: https://github.com/phongdang17183
