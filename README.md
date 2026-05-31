# Imperative Language Compiler

A custom optimizing compiler that translates a simple imperative programming language into an execution-ready virtual machine assembly code. Built using **Python 3.12** and the **PLY (Python Lex-Yacc)** framework, this project demonstrates advanced concepts in lexical analysis, parsing, abstract syntax tree (AST) generation, symbol table management, and low-level code generation.

---

## Project Overview

The compiler processes a structured, strongly-typed imperative language and targets a custom 8-register virtual machine. It features a robust semantic analysis layer to detect and report compilation errors (e.g., re-declarations, undeclared variables, or invalid procedure calls) and outputs highly optimized machine instructions.

### Key Technical Features:
* **Advanced Code Optimization:** Multiplication, division, and modulo operations are implemented using bit-shifting operations (`SHL`, `SHR`), guaranteeing **logarithmic time complexity $O(\log N)$** relative to the argument values.
* **Memory Management & Reference Passing:** Supports multi-dimensional array slicing/indexing and advanced procedure scopes with **pass-by-reference** (IN-OUT parameters).
* **Static Access Control:** Implements compiler-enforced variable attributes including read-only constraints (`I`) and uninitialized safety checks (`O`) within procedure signatures.
* **Deterministic Loop Handling:** `FOR` loops utilize localized iterators with immutable boundaries established at runtime initialization, strictly protected against loop-body modification.

---

## Technical Stack

* **Language:** Python 3.12+
* **Parsing Tools:** PLY 3.11 (Python Lex-Yacc)
* **Target Architecture:** Custom 8-register VM ($r_a$ through $r_h$) with an unbounded arbitrary-precision memory model.

---

## Environment Setup & Requirements

Since this compiler is written in Python, it runs cross-platform. To set up the environment on **Ubuntu / Debian systems**, ensure the following dependencies are installed:

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

