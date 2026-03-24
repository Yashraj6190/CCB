from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class BiquadResult:
    inputs: List[float]
    outputs: List[float]


def biquad_filter(inputs: List[float]) -> BiquadResult:
    """Second-order filter used in HW2 Figure 2.

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
    inp = [100, 5, 500, 20, 250]
    res = biquad_filter(inp)
    print("Biquad sequence simulation (5 cycles)")
    print("n  x[n]    y[n]")
    for i, (x, y) in enumerate(zip(res.inputs, res.outputs), start=1):
        print(f"{i:1d} {x:6.1f} {y:10.6f}")
