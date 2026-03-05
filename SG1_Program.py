# This program was developed using Python on Visual Studio Code, and tested on Thonny.
# Daniel McKinnis, AJ Soma Ravichandran, Matthew Yeager, and Jacob Young
# Date started: 02/25/2026 Date Submitted: 03/09/2026
# CS 4500
# This program is designed to taker user input for number of pills, number of simulation, and a day to track
# This input is checked to ensure appropriate integer values
# The program then simulated the Pill Puzzle question. Starting with N pills, and running R simulations. 
# Each pill is drawn at random. If it is a whole pill, split it in half, take half, and put it back in the bottle. If its a half pill, take it.
# The program answers 3 questions:
#   Q1: Expected number of whole and half pills on given day D.
#   Q2: Which day is most likely the day the last whole pill is taken?
#   Q3: Probability of drawing a hlaf pill on day D.
# The program also displays the possible draw sequence to demonstrate probabilities to users.
# THe data structures used are:
#   - day_freq: a list of length 2*N+1 where day_freq[d] counts how many simulations had their last whole pill taken on day d. Index 0 is unused
#   - results: a dictionary mapping each draw seuqence to its frequency count across R simulations
# Outside resources used:
#   matplotlib: for histogram
#   Python random.randint() 
#   ChatGPT: used for chart styling, line structuring, progress bar implementation, and error checking(found minor syntax errors, such as switching W with H, and calculation errors)
#   w3 schools: used to lookup syntax for dictionary use and function declorations, along with parameter passing
# FOR TESTING ON THONNY, TOOLS->MANAGE PACKAGES-> SEARCH AND INSTALL matplotlib. THIS ENSURES THE GRAPHS / HISTOGRAMS OUTPUT.

import random
import math
import sys
import matplotlib.pyplot as plt

# This function simulates the pill drawing process for N whole pills and D days. It returns the number of whole and half pills on day D, the day when whole pills run out,
# and whether a half pill was drawn on day D. If return_sequence is True, it also returns the sequence of draws (W for whole, H for half) for all days.
def simulate(N, D=None, return_sequence=False):
    
    W = N
    H = 0
    WholePillsOnDayD = 0
    HalfPillsOnDayD = 0
    HalfDrawOnDayD = False
    DayWholeZero = None
    sequence = "" if return_sequence else None

    for day in range(1, 2 * N + 1):

        total = W + H
        RandomPick = random.randint(1, total)
        
        if RandomPick <= W:
            W -= 1
            H += 1
            DrawHalf = False
            if return_sequence:
                sequence += "W"
        else:
            H -= 1
            DrawHalf = True
            if return_sequence:
                sequence += "H"

        if D is not None and day == D:
            WholePillsOnDayD = W
            HalfPillsOnDayD = H
            if DrawHalf:
                HalfDrawOnDayD = True

        if W == 0 and DayWholeZero is None:
            DayWholeZero = day
    
    if return_sequence:
        return WholePillsOnDayD, HalfPillsOnDayD, DayWholeZero, HalfDrawOnDayD, sequence

    return WholePillsOnDayD, HalfPillsOnDayD, DayWholeZero, HalfDrawOnDayD

def progress_bar(current, total, bar_length=40):
    percent = current / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "-" * (bar_length - filled)
    sys.stdout.write(f"\rProgress: |{bar}| {percent:.1%}")
    sys.stdout.flush()

    if current == total:
        print()  # Move to next line when done

# Question 1: Expected pill counts on day D
def expected_WH_on_day_d(TotalWonD, TotalHonD, R):
    avg_whole = TotalWonD / R
    avg_half  = TotalHonD / R
    print("\n--- Question 1: Expected pill counts on day D ---")
    print(f"  Expected whole pills: {avg_whole:.4f}")
    print(f"  Expected half  pills: {avg_half:.4f}")

# Question 2: Most likely day to run out of whole pills
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

    # --- Vertical reference lines ---
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

    # --- Annotations floating above each line ---
    ymax = max(frequencies) * 1.02
    top_gap = ymax * 0.03  # small gap above annotation baseline

    annotation = [
        (min_day,         "#2ECC71", f"Min\n{min_day}",          "right"),
        (max_day,         "#E74C3C", f"Max\n{max_day}",          "left"),
        (avg_day,         "#F39C12", f"Avg\n{avg_day:.2f}",      "right"),
        (most_likely_day, "#C0583A", f"Mode\n{most_likely_day}", "left"),
    ]

    for x_val, color, text, ha in annotation:
        ax.text(x_val, ymax + top_gap, text,
                color=color, fontsize=8.5, fontweight="bold",
                ha=ha, va="bottom", zorder=4,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor=color, linewidth=1.2, alpha=0.9))

    # Leave headroom for annotations
    ax.set_ylim(0, ymax * 1.22)
    ax.set_xlim(0.5, 2 * N + 0.5)

    ax.set_xlabel("Day", fontsize=12, labelpad=6)
    ax.set_ylabel("Frequency", fontsize=12, labelpad=6)
    ax.set_title("Distribution of Day When Last Whole Pill Was Taken",
                 fontsize=14, fontweight="bold", pad=14)

    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=1)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.show()
    
    
# ----------------------------------------------------------
# Question 3: Calculates half-draw probability on day D
# ----------------------------------------------------------

def compute_half_draw_probability(half_draw_count, R):

    # Probability estimate = (# times half drawn on day D) / (total simulations)
    probability = half_draw_count / R

    # Display result clearly to the user
    print("\n--- Question 3: Half-draw probability on day D ---")
    print(f"  Estimated probability of drawing a half pill on day {D}: {probability:.6f}")
    

    
# This function is for demonstrating the non-uniform distribution of sequences for N=4. When the R is small, the chances could be more equally likely, 
# but as R increases, we will see that propbaility of sequences are not equally likely, and some sequences will occur more frequently than others.
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
        


# MAIN
# ==========================================================

if __name__ == "__main__":
    
    N = int(input("Enter the number of whole pills (N): "))
    R = int(input("Enter the number of simulations (R): "))
    D = int(input("Enter the day to analyze (D): "))

    totalWholePillOnDayD = 0
    totalHalfPillOnDayD = 0
    half_draw_count = 0

    day_freq = [0] * (2 * N + 1)

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
    
    expected_WH_on_day_d(totalWholePillOnDayD, totalHalfPillOnDayD, R)
    
    avg_day, most_likely_day, min_day, max_day = compute_last_whole_pill_day(day_freq, R)
    
    plot_last_whole_histogram(day_freq, N, avg_day, most_likely_day, min_day, max_day)
    
    compute_half_draw_probability(half_draw_count, R)
    

    compute_sequence_probability(4, 100000)
