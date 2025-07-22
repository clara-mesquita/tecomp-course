from turing_machine import process_turing_machine
from linear_turing_machine import process_turing_machine_3tapes


def main():
    print("Turing Machine Simulator")
    print("Language: L = {0^k 1^k 2^k | k ≥ 0}")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Single tape Turing machine")
        print("2. Three tape Turing machine")
        print("3. Exit")

        choice = input("Choose option (1-3): ").strip()

        if choice == "3":
            print("Exiting...")
            break
        elif choice in ["1", "2"]:
            input_string = input("Enter string to test (or 'quit' to return): ").strip()

            if input_string.lower() == "quit":
                continue

            # Validate input contains only 0, 1, 2
            if not all(c in "012" for c in input_string):
                print("Error: String must contain only characters '0', '1', '2'")
                continue

            print()

            if choice == "1":
                process_turing_machine(input_string)
            elif choice == "2":
                process_turing_machine_3tapes(input_string)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
