import random
import math

def simulate(N, D):
    W = N
    H = 0
    WonD = 0
    HonD = 0
    HalfDrawOnD = False
    DayZero = None

    for day in range(1, 2 * N + 1):
        pick = random.randint(1, W + H)
        if pick <= W:
            W -= 1
            H += 1
            DrawHalf = False
        else:
            H -= 1
            DrawHalf = True

        if day == D:
            WonD = W
            HonD = H
            if DrawHalf:
                HalfDrawOnD = True

        if W == 0 and DayZero is None:
            DayZero = day

    return WonD, HonD, DayZero, HalfDrawOnD


def question1(TotalWonD, TotalHonD, R):
    avg_whole = TotalWonD / R
    avg_half  = TotalHonD / R
    print("\n--- Question 1: Expected pill counts on day D ---")
    print(f"  Expected whole pills: {avg_whole:.4f}")
    print(f"  Expected half  pills: {avg_half:.4f}")


def question2(DayFreq, N):
    most_likely_day = DayFreq.index(max(DayFreq[1:]), 1)
    print("\n--- Question 2 ---")
    print(f"  Most likely day to run out of whole pills: Day {most_likely_day}")
    
