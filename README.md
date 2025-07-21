# Turing Machine – Foundations of Computer Science

This project is part of the coursework for the **Foundations of Computer Science** class in the Master's program in Computer Science from **State University of Ceará**, taught by **Professor Bonfim**.

## Objective

Implement a Turing Machine that recognizes the following language:

> **L = {0ⁿ 1ⁿ 2ⁿ | n ≥ 0}**

The project includes two versions:

* **Single-tape machine**: a classical simulation using marking and multiple passes.
* **Three-tape machine**: an optimized linear version that copies symbols to auxiliary tapes and compares them directly.

## How to Run

Make sure you're in the same directory as the files and run:

```bash
python main.py
```

## Structure

* `main.py`: entry point that lets you choose between the single-tape and three-tape versions.
* `turing_machine.py`: implementation of the **single-tape** Turing machine.
* `linear_turing_machine.py`: implementation of the **three-tape** Turing machine.

## Example Input

Enter a string like:

```
001122
```

The machine will verify whether the string belongs to the language and display a step-by-step execution trace.