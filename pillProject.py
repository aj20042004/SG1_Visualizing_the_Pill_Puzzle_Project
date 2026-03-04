import sys
import time


def get_valid_int(prompt: str, min_val: int, max_val: int) -> int:
    """
    Prompt user until they enter a valid integer in [min_val, max_val].

    Error messages differentiate:
      1) not a number / not an integer (e.g., letters, decimals, symbols)
      2) integer but out of range
      3) empty input
    """
    while True:
        s = input(prompt).strip()

        if s == "":
            print("Invalid input: no value entered.")
            continue

        # Reject negatives and decimals explicitly; accept only digits
        if not s.isdigit():
            print("Invalid input: please enter an integer (no letters, symbols, or decimals).")
            continue

        value = int(s)
        if value < min_val or value > max_val:
            print(f"Invalid input: number must be between {min_val} and {max_val}.")
            continue

        return value


def show_progress(done: int, total: int, start_time: float,
                  bar_width: int = 30,
                  extra: str = "") -> None:
    """
    In-place progress bar for Thonny console.
    Updates the same line using carriage return.
    """
    total = max(1, total)
    frac = min(max(done / total, 0.0), 1.0)

    filled = int(bar_width * frac)
    bar = "#" * filled + "-" * (bar_width - filled)

    elapsed = time.time() - start_time
    pct = 100.0 * frac

    sys.stdout.write(
        f"\r[{bar}] {done}/{total} ({pct:6.2f}%) | elapsed {elapsed:6.1f}s {extra}   "
    )
    sys.stdout.flush()

    if done >= total:
        print()  # newline when finished


def run_one_simulation_stub(N: int) -> int:
    """
    Placeholder for pill-bottle simulation.

    Return value should be the day (1..2N) when the last whole pill is selected
    (i.e., when you 'run out of whole pills').

    Replace this stub with real simulation logic.
    """
    return N


def main() -> None:
    # One-screen intro
    print("SG1: Pill Puzzle Simulator")
    print("This program simulates the 'Pill Puzzle' R times for a bottle starting with N whole pills.")
    print("It shows progress while running and collects statistics for later display.\n")

    # Get N and R with required ranges and clear prompts
    N = get_valid_int(
        "Enter N (initial whole pills), an integer between 1 and 1000: ",
        1, 1000
    )
    print(f"N accepted: {N} (the bottle starts with {N} whole pills)\n")

    R = get_valid_int(
        "Enter R (number of simulations), an integer between 1 and 10000: ",
        1, 10000
    )
    print(f"R accepted: {R} (the bottle will be simulated {R} times)\n")

    # Run simulations with progress display
    start_time = time.time()
    update_every = max(1, R // 100)  # about 100 progress updates total

    min_day = None
    max_day = None
    sum_day = 0

    for i in range(1, R + 1):
        last_whole_day = run_one_simulation_stub(N)  # replace with real simulation
        sum_day += last_whole_day
        min_day = last_whole_day if min_day is None else min(min_day, last_whole_day)
        max_day = last_whole_day if max_day is None else max(max_day, last_whole_day)
        avg_day = sum_day / i

        if i % update_every == 0 or i == R:
            extra = f"| last-whole day: min={min_day}, avg={avg_day:6.2f}, max={max_day}"
            show_progress(i, R, start_time, bar_width=30, extra=extra)

    # End-of-run message (your real program would now display Q1/Q2/Q3 results)
    print("\nAll simulations completed.")
    input("Press ENTER to end the program.")


if __name__ == "__main__":
    main()