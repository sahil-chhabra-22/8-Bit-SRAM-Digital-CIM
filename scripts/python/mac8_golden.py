#!/usr/bin/env python3
"""Golden model of the FlexDCIM-style unsigned MAC (digital domain).

Per column block: 1b input x w-bit weight (DPU product bits, CBL) -> binary adder tree over N inputs
(14b for N=64, 8b weights) -> shift-and-add over bit-serial input cycles (MSB first, as in the paper).
"""
import random


def decode_ws(wsel: int) -> int:
    """WSEL<2:0> -> WS<7:0> thermometer code: 0 -> 1b weight ... 7 -> 8b weight."""
    assert 0 <= wsel <= 7
    return (1 << (wsel + 1)) - 1


def dcim_mac(inputs, weights, in_bits=8, w_bits=8):
    assert len(inputs) == len(weights)
    assert all(0 <= x < 2 ** in_bits for x in inputs)
    assert all(0 <= w < 2 ** w_bits for w in weights)
    acc = 0
    for b in range(in_bits - 1, -1, -1):
        partial = sum(((x >> b) & 1) * w for x, w in zip(inputs, weights))   # adder-tree output
        acc = (acc << 1) + partial                                            # shift-and-add
    return acc


def reference(inputs, weights):
    return sum(x * w for x, w in zip(inputs, weights))


def required_bits(n, in_bits=8, w_bits=8):
    return (n * (2 ** in_bits - 1) * (2 ** w_bits - 1)).bit_length()


if __name__ == "__main__":
    random.seed(0)
    n = 64
    x = [random.randrange(256) for _ in range(n)]
    w = [random.randrange(256) for _ in range(n)]
    y = dcim_mac(x, w)
    print(f"N={n}  result={y}  reference={reference(x, w)}  match={y == reference(x, w)}")
    print(f"adder-tree width (1b x 8b, N=64): {required_bits(n, 1, 8)} bits")
    print(f"accumulator width (8b x 8b, N=64): {required_bits(n, 8, 8)} bits")
