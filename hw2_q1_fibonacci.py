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


if __name__ == "__main__":
    runs = [(0, 1), (3, 7)]
    for a0, b0 in runs:
        res = fibonacci_steps(a0, b0, 12)
        print(f"Fibonacci start=({a0},{b0}), steps=12")
        print("k  A  B")
        for k, (a, b) in enumerate(res.history):
            print(f"{k:2d} {a:4d} {b:5d}")
        print(f"Final pair after 12 updates: A={res.history[-1][0]}, B={res.history[-1][1]}")
        print()
