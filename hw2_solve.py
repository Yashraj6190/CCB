from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class FibResult:
    start_a: int
    start_b: int
    steps: int
    history: List[Tuple[int, int]]



def fibonacci_steps(a0: int, b0: int, steps: int = 12) -> FibResult:
    """Run exactly `steps` Fibonacci updates: (a,b) <- (b, a+b)."""
    a, b = a0, b0
    history = [(a, b)]
    for _ in range(steps):
        a, b = b, a + b
        history.append((a, b))
    return FibResult(a0, b0, steps, history)


@dataclass
class BiquadResult:
    inputs: List[float]
    outputs: List[float]



def biquad_filter(inputs: List[float]) -> BiquadResult:
    """Second-order filter used in HW2 Figure 2:

    y[n] = (x[n] + x[n-1] + x[n-2] + y[n-1] + y[n-2]) / 8

    Initial delayed values are zero.
    """
    x1 = x2 = 0.0
    y1 = y2 = 0.0
    outputs: List[float] = []

    for x in inputs:
        y = (x + x1 + x2 + y1 + y2) / 8.0
        outputs.append(y)
        x2, x1 = x1, x
        y2, y1 = y1, y

    return BiquadResult(inputs, outputs)


if __name__ == "__main__":
    runs = [(0, 1), (3, 7)]
    for a0, b0 in runs:
        res = fibonacci_steps(a0, b0, 12)
        print(f"Fibonacci start=({a0},{b0}), steps=12")
        print("k  A  B")
        for k, (a, b) in enumerate(res.history):
            print(f"{k:2d} {a:3d} {b:4d}")
        print(f"Final pair after 12 updates: A={res.history[-1][0]}, B={res.history[-1][1]}")
        print()

    inp = [100, 5, 500, 20, 250]
    bq = biquad_filter(inp)
    print("Biquad sequence simulation")
    print("n  x[n]  y[n]")
    for i, (x, y) in enumerate(zip(bq.inputs, bq.outputs), start=1):
        print(f"{i:1d} {x:5.1f} {y:10.6f}")
