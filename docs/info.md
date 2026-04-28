<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This design implements a simple synchronous BCD calculator. Two 4-bit operands (A and B) are incremented using input buttons. The circuit continuously computes their sum and outputs the result in decimal format, split into tens and ones digits.

## How to test

- Apply reset to initialize both operands to 0.
- Use ui[0] to increment operand A.
- Use ui[1] to increment operand B.
- Observe the outputs:
1. uio_out shows the current values of A and B.
2. uo_out shows the sum in BCD (lower 4 bits = ones, upper 4 bits = tens).
- Verify correct behavior including overflow (e.g., 9 → 0 wrap-around).

## External hardware

No external hardware is required. The design can be tested entirely using simulation or within the Tiny Tapeout framework.
