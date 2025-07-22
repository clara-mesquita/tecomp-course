"""
Implementing Linear (3 tapes) Turing Machine to recognize L = {0^k 1^k 2^k | k ≥ 0}

The algorithm is as follows:
- The chain is written on first tape
- Then when '1' is found, is written on 2nd tape 
- Then '2's are written on 3rd tape 
- The quantity of 2nd and 3rd tapes are compared with the quantity of '2's of first tape
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
    # Valores‑padrão (não escreve nada, não move)
    written1, written2, written3 = symbol1, symbol2, symbol3
    new_state = state
    dir1 = dir2 = dir3 = "S"

    # ---------------------- CÓPIA DOS 0s ----------------------
    if state == "q0":
        if symbol1 == "$":
            dir1 = "R"  # pula marcador
        elif symbol1 == "0":
            written2 = "0"  # copia 0 p/ fita‑2
            dir1 = dir2 = "R"
        elif symbol1 == "1":
            new_state = "q1"  # passou p/ parte dos 1s
        elif symbol1 == "_":  # string vazia
            new_state = "q2"
        else:
            new_state = "qrej"

    # ---------------------- CÓPIA DOS 1s ----------------------
    elif state == "q1":
        if symbol1 == "1":
            written3 = "1"  # copia 1 p/ fita‑3
            dir1 = dir3 = "R"
        elif symbol1 == "2":
            new_state = "q2"  # hora de comparar
        else:
            new_state = "qrej"

    # ---------- rebobinar fitas 2 e 3 até o "$" -------------
    elif state == "q2":
        # Volta as cabeças até encontrar o marcador $
        if symbol2 != "$":
            dir2 = "L"
        if symbol3 != "$":
            dir3 = "L"

        # Quando ambas voltarem ao $, avança‑as 1 passo e começa a comparar
        if symbol2 == "$" and symbol3 == "$":
            dir2 = dir3 = "R"
            new_state = "q3"

        dir1 = "S"  # fita‑1 já está no primeiro 2 (ou no _ se k == 0)

    # -------------------- COMPARAÇÃO --------------------------
    elif state == "q3":
        if symbol1 == "2" and symbol2 == "0" and symbol3 == "1":
            dir1 = dir2 = dir3 = "R"  # contagem bateu: avança
        elif symbol1 == "_" and symbol2 == "_" and symbol3 == "_":
            new_state = "qacc"  # todas esgotadas
        else:
            new_state = "qrej"  # qualquer divergência

    # -------------------- Estados finais ---------------------
    # (qacc e qrej apenas mantêm‑se)

    # Grava e move as cabeças
    tape1 = write_symbol(head1, tape1, written1)
    tape2 = write_symbol(head2, tape2, written2)
    tape3 = write_symbol(head3, tape3, written3)

    if dir1 != "S":
        head1 = move_head(tape1, head1, dir1)
    if dir2 != "S":
        head2 = move_head(tape2, head2, dir2)
    if dir3 != "S":
        head3 = move_head(tape3, head3, dir3)


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

