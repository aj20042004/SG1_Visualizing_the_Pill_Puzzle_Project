import random
import math
import sys

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
def compute_last_whole_pill_day(DayFreq, N):
    most_likely_day = DayFreq.index(max(DayFreq[1:]), 1)
    print("\n--- Question 2 ---")
    print(f"  Most likely day to run out of whole pills: Day {most_likely_day}")
    

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
    

    
    
    
    compute_sequence_probability(4, 100000)  