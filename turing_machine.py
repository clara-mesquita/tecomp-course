"""
Implementing Classic (1 tape) Turing Machine to recognize L = {0^k 1^k 2^k | k ≥ 0}

The algorithm is as follows:
- Marks '$' as tape start and '_' as final symbol
- Looks for first '0' and then marks with 'X'
- Then looks for the first '1' and marks with 'Y'; do the same with '2', marking 'Z'
- Then verifies if the tape is all marked
"""


def load_chain_single(w):
    tape = ["$"] + list(w) + ["_"]  # Using '$' to mark start and '_' to mark end
    return tape


def write_symbol(head, tape, new_symbol):
    if head < len(tape):
        tape[head] = new_symbol
    return tape


def move_head_single(tape, head, direction):
    if (
        direction == "R" and head < len(tape) - 1
    ):  # Moves for right in tape if is not the end of the tape
        head += 1
    elif (
        direction == "L" and head > 0
    ):  # Moves for left if is not the start of the tape
        head -= 1
    elif direction == "L" and head == 0:  # When there's some verification going on #change for S
        return
    return head


def print_configuration_single(
    prev_state, symbol, current_state, written_symbol, direction
):
    print(
        f"      Config: {prev_state} ---{symbol}, {written_symbol}/{direction}---> {current_state}\n"
    )


def print_current_tape(tape, head):
    tape_str = "".join(tape)
    print(f"        Tape: {tape_str}")
    spaces = " " * (14 + head)
    print(f"{spaces}^")
    print()


def do_transition_single(head, state, symbol, tape):
    written_symbol = symbol  # For default, doesn't write anything
    new_state = state  # And don't change state
    direction = "L"  # For final states

    if state == "q0":  # Initial state
        if symbol == "$":  # Tape start
            direction = "R"
        elif symbol == "_":  # Handle empty chain (k == 0)
            new_state = "qacc"
        elif symbol == "0":  # Marks
            written_symbol = "X"
            direction = "R"
            new_state = "q1"
        elif symbol == "X":
            direction = "R"
            new_state = "q4"
        else:
            new_state = "qrej"

    elif state == "q1":  # Searchs for '1'
        if symbol == "0":
            direction = "R"
        elif symbol == "Y":
            direction = "R"
        elif symbol == "1":
            written_symbol = "Y"  # Marks
            direction = "R"
            new_state = "q2"
        elif symbol == "_":  # Didn't find any '1'
            new_state = "qrej"
        else:
            new_state = "qrej"

    elif state == "q2":  # Searchs for '2'
        if symbol == "1":
            direction = "R"
        elif symbol == "Z":
            direction = "R"
        elif symbol == "2":
            written_symbol = "Z"  # Marks
            direction = "L"
            new_state = "q3"
        elif symbol == "_":  # Didn't find any '2'
            new_state = "qrej"
        else:
            new_state = "qrej"

    elif state == "q3":
        if symbol == "$":  # If found start
            direction = "R"
            new_state = "q0"
        else:
            direction = "L"

    elif state == "q4":  # Verifies if all '0' were processed
        if symbol == "X":
            direction = "R"
        elif symbol == "0":
            written_symbol = "X"
            direction = "R"
            new_state = "q1"
        elif symbol == "Y":
            direction = "R"
            new_state = "q5"
        elif symbol == "_":
            new_state = "qacc"
        else:
            new_state = "qrej"

    elif state == "q5":  # Verifies if all '1' were processed
        if symbol == "Y":
            direction = "R"
        elif symbol == "1":
            new_state = "qrej"  # '1' leftover
        elif symbol == "Z":
            direction = "R"
            new_state = "q6"
        elif symbol == "_":
            new_state = "qrej"  # End of tape without '2'
        else:
            new_state = "qrej"

    elif state == "q6":  # Verifies if all '2' were processed
        if symbol == "Z":
            direction = "R"
        elif symbol == "2":
            new_state = "qrej"  # '2' leftover
        elif symbol == "_":
            new_state = "qacc"
        else:
            new_state = "qrej"

    print_configuration_single(state, symbol, new_state, written_symbol, direction)
    tape = write_symbol(head, tape, written_symbol)
    head = move_head_single(tape, head, direction)
    print_current_tape(tape, head)

    return head, tape, new_state


def process_turing_machine(w):
    """Processa a cadeia usando uma fita"""
    print(f"\n=== PROCESSANDO COM UMA FITA: '{w}' ===")

    tape = load_chain_single(w)
    current_state = "q0"
    head = 0
    steps = 0

    print_current_tape(tape, head)

    while current_state not in ["qacc", "qrej"]:
        current_symbol = tape[head]
        head, tape, current_state = do_transition_single(
            head, current_state, current_symbol, tape
        )
        steps += 1

    result = "ACEITA" if current_state == "qacc" else "REJEITA"
    print(f"Resultado: {result} (em {steps} passos)")
    return current_state == "qacc"
