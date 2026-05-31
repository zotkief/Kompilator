# Imperative Language Compiler

[cite_start]A custom optimizing compiler that translates a simple imperative programming language into an execution-ready virtual machine assembly code[cite: 3]. Built using **Python 3.12** and the **PLY (Python Lex-Yacc)** framework, this project demonstrates advanced concepts in lexical analysis, parsing, abstract syntax tree (AST) generation, symbol table management, and low-level code generation.

---

## Project Overview

[cite_start]The compiler processes a structured, strongly-typed imperative language and targets a custom 8-register virtual machine[cite: 3, 142]. [cite_start]It features a robust semantic analysis layer to detect and report compilation errors (e.g., re-declarations, undeclared variables, or invalid procedure calls) [cite: 4] [cite_start]and outputs highly optimized machine instructions[cite: 4, 5].

### Key Technical Features:
* [cite_start]**Advanced Code Optimization:** Multiplication, division, and modulo operations are implemented using bit-shifting operations (`SHL`, `SHR`), guaranteeing **logarithmic time complexity $O(\log N)$** relative to the argument values[cite: 5, 149, 607].
* [cite_start]**Memory Management & Reference Passing:** Supports multi-dimensional array slicing/indexing [cite: 19, 20] [cite_start]and advanced procedure scopes with **pass-by-reference** (IN-OUT parameters)[cite: 21].
* [cite_start]**Static Access Control:** Implements compiler-enforced variable attributes including read-only constraints (`I`) [cite: 24] [cite_start]and uninitialized safety checks (`O`) [cite: 25] within procedure signatures.
* [cite_start]**Deterministic Loop Handling:** `FOR` loops utilize localized iterators with immutable boundaries established at runtime initialization, strictly protected against loop-body modification[cite: 26, 27, 28].

---

## Technical Stack

* **Language:** Python 3.12+
* **Parsing Tools:** PLY 3.11 (Python Lex-Yacc)
* [cite_start]**Target Architecture:** Custom 8-register VM ($r_a$ through $r_h$) with an unbounded arbitrary-precision memory model[cite: 142, 143].

---

## Environment Setup & Requirements

Since this compiler is written in Python, it runs cross-platform. [cite_start]To set up the environment on **Ubuntu / Debian systems**, ensure the following dependencies are installed[cite: 8]:

```bash
# Update package list and install Python 3 with pip
sudo apt update
sudo apt install python3.12 python3-pip -y

# Install the PLY (Lex-Yacc) framework
pip install ply==3.11
```

---

## Usage & Execution

The compiler accepts data and outputs the generated assembly strictly via file paths. Run the compiler using the following command:

```bash
python -m main <input_source_file> <output_target_file>

```

### Example

To compile a prime factorization program:

```bash
python -m main examples/factorization.imp output.mr

```

---

## Language Specification Highlights

* 
**Arithmetic:** Operates natively on natural numbers. Features safe subtraction (flooring at 0) and zero-division handling (returns 0 with 0 remainder).


* 
**Arrays:** Supports custom-indexed ranges (e.g., `tab[10:30]` instantiates a 21-element array) with static boundary verification at compile time.


* 
**Comments:** Uses Python-style inline comments starting with `#`.

