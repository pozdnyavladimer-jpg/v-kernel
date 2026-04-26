# V-Kernel Stability Scanner — Demo Results

## Purpose

This demo shows the first working proof-of-concept for V-Kernel as a stability scanner.

The scanner does not operate as a traditional linter.

It converts code into a behavioral state, runs a convergence model, and reports structural stability.

---

## Demo Inputs

### 1. Stable Code

File:

    examples/good_code.py

Result:

    Stability: HIGH
    Label: stable structure
    Mode: yellow_struct

---

### 2. Infinite Loop

File:

    examples/bad_loop.py

Result:

    Stability: LOW
    Label: instability detected
    Mode: red_mass

---

### 3. Bare Except

File:

    examples/bare_except.py

Result:

    Stability: LOW
    Label: instability detected
    Mode: red_mass

---

## Core Result

    good_code.py   -> HIGH
    bad_loop.py    -> LOW
    bare_except.py -> LOW

---

## Meaning

code -> state -> convergence -> stability report

---

## Status

First proof-of-concept completed.
