"""
Implementing Linear (3 tapes) Turing Machine to recognize L = {0^k 1^k 2^k | k ≥ 0}

The algorithm is as follows:

"""

def load_chain(w):
    tape1 = ["$"] + list(w) + ["_"]  # Initial chain with start marker
    tape2 = ["$"] + ["_"] # This tape will save '0's 
    tape3 = ["$"] + ["_"] # This tape will save '1's 
    return tape1, tape2, tape3


def write_symbol(head, tape, new_symbol):
    # Extend tape if necessary
    while head >= len(tape):
        tape.append("_")
    tape[head] = new_symbol
    return tape


def move_head(tape, head, direction):
    if direction == "R":
        head += 1
        # Extend tape if necessary
        while head >= len(tape):
            tape.append("_")
    elif direction == "L" and head > 0:
        head -= 1
    elif direction == "S": # Head don't move 
        return head
    return head


def print_configuration_three(
    prev_state,
    symbol1,
    symbol2,
    symbol3,
    current_state,
    written1,
    written2,
    written3,
    dir1,
    dir2,
    dir3,
):
    print(
        f"      Config Tape 1: ({prev_state}) --({symbol1} → {written1}, {dir1})--> ({current_state})\n"
        f"      Config Tape 2: ({prev_state}) --({symbol2} → {written2}, {dir2})--> ({current_state})\n"
        f"      Config Tape 3: ({prev_state}) --({symbol3} → {written3}, {dir3})--> ({current_state})\n\n"
    )


def print_tapes_three(tape1, tape2, tape3, head1, head2, head3):
    """Print current state of three tapes"""
    tape1_str = "".join(tape1)
    tape2_str = "".join(tape2)
    tape3_str = "".join(tape3)

    print(f"      Tape 1 (Original): {tape1_str}")
    spaces1 = " " * (25 + head1)
    print(f"{spaces1}^")

    print(f"      Tape 2 ('0's): {tape2_str}")
    spaces2 = " " * (21 + head2)
    print(f"{spaces2}^")

    print(f"      Tape 3 ('1's): {tape3_str}")
    spaces3 = " " * (21 + head3)
    print(f"{spaces3}^")
    print()


def do_transition_three(
    head1, head2, head3, state, symbol1, symbol2, symbol3, tape1, tape2, tape3
):
    written1, written2, written3 = (
        symbol1,
        symbol2,
        symbol3,
    )  # Default
    new_state = state
    dir1, dir2, dir3 = "S", "S", "S"  # Don't move

    if state == "q0":  # Reads 0s and copy to tape 2
        if symbol1 == "$":  # Skip start marker
            dir1 = "R"
        elif symbol1 == "0":
            written2 = "0"  # Copy 0 to tape 2
            dir1, dir2 = "R", "R"
        elif symbol1 == "1":
            new_state = "q1"  # Switch to reading 1s
        elif symbol1 == "_":  # Empty string (only $ followed by _)
            new_state = "q2"  # Go directly to marking phase
        else:
            new_state = "qrej"

    elif state == "q1":  # Read 1s and copy to tape 3
        if symbol1 == "1":
            written3 = "1"  # Copy 1 to tape 3
            dir1, dir3 = "R", "R"
        elif symbol1 == "2":
            new_state = "q2"  # Switch to reading 2s
        elif symbol1 == "_":  # No 2s found
            new_state = "qrej"
        else:
            new_state = "qrej"

    elif state == "q2":  # Mark first 2 and prepare for comparison
        if symbol1 == "2":
            written1 = "$"  # Mark first 2
            dir1 = "R"
            new_state = "q3"  # Move to return phase
        elif symbol1 == "_":  # Empty case (0^k 1^k with k=0)
            new_state = "q3"  # Go to return phase
        else:
            new_state = "qrej"

    elif state == "q3":  # Return heads 2 and 3 to start positions
        if head2 > 1 or head3 > 1:  # Return tapes 2 and 3 to start
            if head2 > 1:
                dir2 = "L"
            if head3 > 1:
                dir3 = "L"
        else:
            # Tapes 2 and 3 at start, move to first data position
            if tape2[1] != "_" or tape3[1] != "_":  # Have data to compare
                dir2, dir3 = "R", "R"
                new_state = "q4"
            else:  # Empty case, check if tape1 also empty
                if symbol1 == "_":
                    new_state = "qacc"  # Accept empty string
                else:
                    new_state = "qrej"

    elif state == "q4":  # Compare 0s, 1s, and 2s counts
        if symbol2 == "0" and symbol3 == "1" and symbol1 == "2":
            # All three symbols present, advance all
            dir1, dir2, dir3 = "R", "R", "R"
        elif symbol2 == "_" and symbol3 == "_" and symbol1 == "_":
            # All reached end simultaneously - accept
            new_state = "qacc"
        else:
            # Counts don't match - reject
            new_state = "qrej"

    elif state == "qacc":  # Accept state
        pass  # Stay in accept state

    elif state == "qrej":  # Reject state
        pass  # Stay in reject state

    print_configuration_three(
        state,
        symbol1,
        symbol2,
        symbol3,
        new_state,
        written1,
        written2,
        written3,
        dir1,
        dir2,
        dir3,
    )

    tape1 = write_symbol(head1, tape1, written1)
    tape2 = write_symbol(head2, tape2, written2)
    tape3 = write_symbol(head3, tape3, written3)

    if dir1 != "S":
        head1 = move_head(tape1, head1, dir1)
    if dir2 != "S":
        head2 = move_head(tape2, head2, dir2)
    if dir3 != "S":
        head3 = move_head(tape3, head3, dir3)

    print_tapes_three(tape1, tape2, tape3, head1, head2, head3)

    return head1, head2, head3, new_state, written1, written2, written3, tape1, tape2, tape3


def process_turing_machine_3tapes(w):
    print(f"\n=== PROCESSING WITH THREE TAPES: '{w}' ===")

    tape1, tape2, tape3 = load_chain(w)

    current_state = "q0"  
    head1, head2, head3 = 0, 1, 1  # Start at beginning of tape1, skip markers on tapes 2,3
    steps = 0

    print_tapes_three(tape1, tape2, tape3, head1, head2, head3)

    while current_state not in ["qacc", "qrej"]: 
        print(f"\n      === {steps + 1}th STEP ===\n")
        symbol1 = tape1[head1] if head1 < len(tape1) else "_"
        symbol2 = tape2[head2] if head2 < len(tape2) else "_"
        symbol3 = tape3[head3] if head3 < len(tape3) else "_"

        head1, head2, head3, current_state, symbol1, symbol2, symbol3, tape1, tape2, tape3 = do_transition_three(
            head1,
            head2,
            head3,
            current_state,
            symbol1,
            symbol2,
            symbol3,
            tape1,
            tape2,
            tape3,
        )
        steps += 1

    result = "ACCEPT" if current_state == "qacc" else "REJECT"
    print(f"Result: {result} (in {steps} steps)")
    return current_state == "qacc"

