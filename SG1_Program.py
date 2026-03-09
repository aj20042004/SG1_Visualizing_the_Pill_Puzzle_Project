# Developed using Python in Visual Studio Code and tested in Thonny.
#
# Authors:
# Daniel McKinnis, AJ Soma Ravichandran, Matthew Yeager, Jacob Young
#
# Course: CMP SCI 4500
# Date Started: 02/25/2026
# Date Submitted: 03/09/2026
#
# Program Description:
# This program simulates the Pill Puzzle. It accepts user input for:
#   1. Initial number of pills (N)
#   2. Number of simulations (R)
#   3. Specific day to track (D)
# All inputs are validated to ensure they are valid integers.
#
# Simulation Logic:
# The simulation starts with N whole pills. In each draw:
#   1. Whole pill - split into two halves, one half taken, one half returned.
#   2. Half pill  - taken from the bottle.
#
# Questions Answered:
#   Q1: Expected number of whole and half pills on day D.
#   Q2: Most likely day the last whole pill is taken.
#   Q3: Probability of drawing a half pill on day D.
#
# Data Structures:
#   day_freq - List where day_freq[d] counts simulations where the last whole pill
#              was taken on day d.
#   results  - Dictionary mapping draw sequences to their frequency.
#
# External Resources:
#   matplotlib - Used for charts and histograms.
#   random.randint() - Used for random pill selection.
#   ChatGPT - Assisted with chart formatting, structure, and minor syntax fixes.
#   W3Schools - Referenced for Python syntax and dictionaries.
#
# Note for Thonny Users:
# Install matplotlib via Tools -> Manage Packages -> Search "matplotlib".

# Import necessary libraries
import random
import sys
import matplotlib.pyplot as plt


# This function simulates the pill drawing process starting with N whole pills.
# The simulation runs until all pills have been consumed.
#
# The function tracks:
#   - The number of whole pills and half pills remaining on day D
#   - The day when the last whole pill is taken
#   - Whether a half pill was drawn on day D
#
# If return_sequence is set to True, the function also returns the full
# sequence of draws for the entire simulation, where:
#   W = whole pill drawn
#   H = half pill drawn
def simulate(N, D=None, return_sequence=False):
    
    # Initialize the bottle with N whole pills and 0 half pills
    W = N
    H = 0
    WholePillsOnDayD = 0
    HalfPillsOnDayD = 0
    HalfDrawOnDayD = False
    DayWholeZero = None
    sequence = "" if return_sequence else None

    # Simulate the process for 2*N days (maximum possible duration)
    for day in range(1, 2 * N + 1):

        total = W + H
        RandomPick = random.randint(1, total)
        
        # If the random pick is less than or equal to the number of whole pills, we draw a whole pill.
        if RandomPick <= W:
            W -= 1
            H += 1
            DrawHalf = False
            if return_sequence:
                sequence += "W"
                
        # If the random pick is greater than the number of whole pills, we draw a half pill.
        else:
            H -= 1
            DrawHalf = True
            if return_sequence:
                sequence += "H"
        
        # Check if we are on day D to record the number of whole and half pills, and whether a half pill was drawn.
        if D is not None and day == D:
            WholePillsOnDayD = W
            HalfPillsOnDayD = H
            if DrawHalf:
                HalfDrawOnDayD = True

        # Check if all whole pills have been taken and record the day if this is the first time it happens.
        if W == 0 and DayWholeZero is None:
            DayWholeZero = day
    
    # If return_sequence is True, we return the collected statistics along with the full sequence of draws.
    if return_sequence:
        return WholePillsOnDayD, HalfPillsOnDayD, DayWholeZero, HalfDrawOnDayD, sequence

    # If return_sequence is False, we return only the statistics without the sequence.
    return WholePillsOnDayD, HalfPillsOnDayD, DayWholeZero, HalfDrawOnDayD


# Displays a progress bar in the console showing the percentage of simulations completed.
def progress_bar(current, total, bar_length=40):
    percent = current / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "-" * (bar_length - filled)
    sys.stdout.write(f"\rProgress: |{bar}| {percent:.1%}")
    sys.stdout.flush()

    if current == total:
        print()  # Move to next line when done


# The function calculates the expected number of whole pills and half pills remaining on a specified day D. 
# The totals collected from all simulations are divided by the total number of simulations (R) to compute 
# the average values. The results are printed to the console in a clear format for the user to interpret.
def expected_WH_on_day_d(TotalWonD, TotalHonD, R):
    avg_whole = TotalWonD / R
    avg_half  = TotalHonD / R
    print("\n--- Question 1: Expected pill counts on day D ---")
    print(f"  Expected whole pills: {avg_whole:.4f}")
    print(f"  Expected half  pills: {avg_half:.4f}")


# This function analyzes the frequency data for the day when the last whole pill was taken.
# Using the day frequency list, the function determines:
#   - The earliest possible day (minimum)
#   - The latest possible day (maximum)
#   - The average day across all simulations
#   - The most likely day (mode) based on highest frequency
# These statistics are displayed to the user and returned for use in
# visualizations such as the histogram. 
def compute_last_whole_pill_day(day_freq, R):
    print("\n--- Question 2: Analysis of Last Whole Pill Day ---")

    # Collect all days based on frequency
    days_list = []
    for day, freq in enumerate(day_freq):
        if day != 0:
            days_list.extend([day] * freq)

    # Statistics
    min_day = min(days_list)
    max_day = max(days_list)
    avg_day = sum(days_list) / R
    most_likely_day = day_freq.index(max(day_freq[1:]), 1)

    print(f"  Minimum day: {min_day}")
    print(f"  Maximum day: {max_day}")
    print(f"  Average day: {avg_day:.4f}")
    print(f"  Most likely day: {most_likely_day}")

    return avg_day, most_likely_day, min_day, max_day
    

# The function generates and displays a histogram that visualizes the distribution of the day when
# the last whole pill was taken across all simulations. The histogram highlights important statistics
# such as the minimum day, maximum day, average day, and the most likely day using vertical lines
# and annotations to help users easily interpret the results.
def plot_last_whole_histogram(day_freq, N, avg_day, most_likely_day, min_day, max_day):
    
    print("\nDisplaying histogram...")
    days = list(range(1, 2 * N + 1))
    frequencies = day_freq[1:]

    fig, ax = plt.subplots(figsize=(12, 6))

    # Base bars in a neutral blue-grey
    bars = ax.bar(days, frequencies, color="#7EB8D4", edgecolor="white", linewidth=0.4, zorder=2)

    # Highlight the most-likely-day bar in a warm accent color
    bars[most_likely_day - 1].set_facecolor("#E8825A")
    bars[most_likely_day - 1].set_edgecolor("#C0583A")

    # Vertical reference lines
    line_cfg = [
        ("Min",         min_day,         "#2ECC71", "--", 1.8),
        ("Max",         max_day,         "#E74C3C", "--", 1.8),
        ("Avg",         avg_day,         "#F39C12", "-",  2.2),
        ("Most Likely", most_likely_day, "#C0583A", "-",  2.2),
    ]

    for label, xval, color, ls, lw in line_cfg:
        display = f"{xval:.2f}" if isinstance(xval, float) else str(xval)
        ax.axvline(x=xval, color=color, linestyle=ls, linewidth=lw,
                   label=f"{label}: {display}", zorder=3)

    # Annotations floating above each line with a small gap
    ymax = max(frequencies) * 1.02
    
    # small gap above annotation baseline
    top_gap = ymax * 0.03  

    # Define annotations for each statistic with appropriate colors and alignment
    annotation = [
        (min_day,         "#2ECC71", f"Min\n{min_day}",          "right"),
        (max_day,         "#E74C3C", f"Max\n{max_day}",          "left"),
        (avg_day,         "#F39C12", f"Avg\n{avg_day:.2f}",      "right"),
        (most_likely_day, "#C0583A", f"Mode\n{most_likely_day}", "left"),
    ]
    
    # Loop through each annotation and place it above the corresponding line with a styled background box
    for x_val, color, text, ha in annotation:
        ax.text(x_val, ymax + top_gap, text,
                color=color, fontsize=8.5, fontweight="bold",
                ha=ha, va="bottom", zorder=4,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor=color, linewidth=1.2, alpha=0.9))

    # Leave headroom for annotations
    ax.set_ylim(0, ymax * 1.22)
    ax.set_xlim(0.5, 2 * N + 0.5)

    # Chart styling
    ax.set_xlabel("Day", fontsize=12, labelpad=6)
    ax.set_ylabel("Frequency", fontsize=12, labelpad=6)
    ax.set_title("Distribution of Day When Last Whole Pill Was Taken",
                 fontsize=14, fontweight="bold", pad=14)

    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=1)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.show()
    
    
# The function calculates and prints the probability of drawing a half pill
# on the specified day D based on simulation results.
def compute_half_draw_probability(half_draw_count, R):

    # Probability estimate = (# times half drawn on day D) / (total simulations)
    probability = half_draw_count / R

    # Display result clearly to the user
    print("\n--- Question 3: Half-draw probability on day D ---")
    print(f"  Estimated probability of drawing a half pill on day {D}: {probability:.6f}")
    

    
# The function demonstrates that the possible pill-draw sequences are not uniformly distributed. 
# For a given number of pills (N) and simulations (R), the function runs simulations and records how often 
# each sequence of draws occurs. The results are then sorted by frequency and displayed along with their probabilities 
# to show that some sequences occur more often than others.
def compute_sequence_probability(N,R):

    results = {}
    
    print("=" * 50)
    print(f"      Running Sequence Probability: N={N}, R={R}       ")
    print("=" * 50)
    
    for i in range(R):
        _, _, _, _, sequence = simulate(N, return_sequence=True)
        results[sequence] = results.get(sequence, 0) + 1

    # Sort by frequency to show they aren't equally likely
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Sequence':<12} | {'Occurrences':<12} | {'Probability'}")
    print("-" * 50)
    for seq, count in sorted_results:
        prob = (count / R) * 100
        print(f"{seq:<12} | {count:<12} | {prob:>6.2f}%")
        

# Prompts the user to enter a valid integer within a specified range.
# The function repeatedly asks for input until a correct value is provided.
# It handles several types of invalid input, including:
#   - Empty input
#   - Non-integer input (letters, decimals, symbols)
#   - Integers outside the allowed range
# Once a valid value is entered, the function returns the integer. 
def get_valid_int(prompt: str, min_val: int, max_val: int) -> int:
    
    while True:
        
        s = input(prompt).strip()

        if s == "":
            print("Error: No value entered. Please enter a whole number.\n")
            continue

        if not s.isdigit():
            print("Error: Invalid input. Please enter a whole number (no letters, decimals, negative numbers or symbols).\n")
            continue

        value = int(s)

        if not (min_val <= value <= max_val):
            print(f"Error: Value out of range. Please enter a number between {min_val} and {max_val} (inclusive).\n")
            continue

        return value
        


# =====================================================================================================================================
# MAIN
# =====================================================================================================================================

if __name__ == "__main__":
    
    # Welcome message and input prompts
    print("\n")
    print("-" * 100)
    print("SG1: Pill Puzzle Simulator")
    print("-" * 100)
    
    print(
"""This program explores the classic probability problem known as the "Pill Puzzle".

You start with a bottle containing N whole pills. Each day you must take half of a pill.
The bottle is assumed to be random: whenever you reach in, each pill (whole or half)
remaining in the bottle has an equal chance of being selected.

Daily process:
1. If a whole pill is selected:
  - The pill is split into two halves
  - One half is taken
  - The other half is returned to the bottle

2. If a half pill is selected:
  - The half pill is taken and nothing is returned to the bottle

This process continues for 2 * N days until all pills have been consumed.

The program runs this experiment many times using computer simulation and
collects statistics to help answer several probability questions, including:

1. The expected number of whole pills and half pills remaining on a chosen day.
2. Which day is most likely to be the day when the last whole pill is taken.
3. The probability of drawing a half pill on a chosen day.

The program will also display a histogram showing when the last whole pill
was taken across all simulations.

You will now be asked to enter:
1. N - the number of whole pills in the bottle
2. R - the number of simulations to run
3. D - the day to analyze

After all simulations finish, the program will display the results.
"""
)
    
    # Get user inputs with validation
    N = get_valid_int("Enter the number of whole pills (must be between 1 and 1000): ", 1, 1000)
    print(f"Input accepted: {N} whole pills will be placed in the bottle.\n")
    
    R = get_valid_int("Enter the number of simulations to run (must be between 1 and 10000): ", 1, 10000)
    print(f"Input accepted: The simulation will run {R} times.\n")
    
    D = get_valid_int(f"Enter the day to analyze (1–{2 * N}): ", 1, 2 * N)
    print(f"Input accepted: Statistics will be calculated for day {D}.\n")

    # Initialize variables for statistics
    totalWholePillOnDayD = 0
    totalHalfPillOnDayD = 0
    half_draw_count = 0
    day_freq = [0] * (2 * N + 1)

    # Run R simulations and collect statistics for each simulation
    for i in range(1, R + 1):

        WholePillsOnDayD, HalfPillsOnDayD, DayWholeZero, HalfDrawOnDayD = simulate(N, D)

        totalWholePillOnDayD += WholePillsOnDayD
        totalHalfPillOnDayD += HalfPillsOnDayD

        if HalfDrawOnDayD:
            half_draw_count += 1

        day_freq[DayWholeZero] += 1

        # Update progress every 1% (prevents slowdown)
        step = max(1, R // 100)

        if i % step == 0 or i == R:
            progress_bar(i, R)
    
    # Analyze and display results for Q1, Q2, Q3, and sequence probabilities
    expected_WH_on_day_d(totalWholePillOnDayD, totalHalfPillOnDayD, R)
    avg_day, most_likely_day, min_day, max_day = compute_last_whole_pill_day(day_freq, R)
    plot_last_whole_histogram(day_freq, N, avg_day, most_likely_day, min_day, max_day)
    compute_half_draw_probability(half_draw_count, R)
    compute_sequence_probability(4, 100000)
    
    # End of program message
    print("\nAll simulations completed.")
    input("Press ENTER to end the program.")
