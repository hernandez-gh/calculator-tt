# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def pulse_button(dut, bit):
    dut.ui_in.value = dut.ui_in.value | (1 << bit)
    await RisingEdge(dut.clk)
    dut.ui_in.value = dut.ui_in.value & ~(1 << bit)
    await RisingEdge(dut.clk)


def decode_outputs(uo_out):
    value = int(uo_out)
    ones = value & 0xF
    tens = (value >> 4) & 0xF
    return tens, ones


def decode_operands(uio_out):
    value = int(uio_out)
    a = value & 0xF
    b = (value >> 4) & 0xF
    return a, b


@cocotb.test()
async def test_calculadora(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    dut.rst_n.value = 0
    await Timer(50, units="ns")
    dut.rst_n.value = 1

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    a, b = decode_operands(dut.uio_out.value)
    tens, ones = decode_outputs(dut.uo_out.value)

    assert a == 0, f"operandA esperado 0, obtenido {a}"
    assert b == 0, f"operandB esperado 0, obtenido {b}"
    assert tens == 0 and ones == 0, f"suma esperada 00, obtenida {tens}{ones}"

    # Incrementar A tres veces
    for _ in range(3):
        await pulse_button(dut, 0)

    a, b = decode_operands(dut.uio_out.value)
    tens, ones = decode_outputs(dut.uo_out.value)

    assert a == 3, f"operandA esperado 3, obtenido {a}"
    assert b == 0, f"operandB esperado 0, obtenido {b}"
    assert tens == 0 and ones == 3, f"suma esperada 03, obtenida {tens}{ones}"

    # Incrementar B cuatro veces
    for _ in range(4):
        await pulse_button(dut, 1)

    a, b = decode_operands(dut.uio_out.value)
    tens, ones = decode_outputs(dut.uo_out.value)

    assert a == 3, f"operandA esperado 3, obtenido {a}"
    assert b == 4, f"operandB esperado 4, obtenido {b}"
    assert tens == 0 and ones == 7, f"suma esperada 07, obtenida {tens}{ones}"

    # Llevar A a 9
    for _ in range(6):
        await pulse_button(dut, 0)

    a, b = decode_operands(dut.uio_out.value)
    tens, ones = decode_outputs(dut.uo_out.value)

    assert a == 9, f"operandA esperado 9, obtenido {a}"
    assert b == 4, f"operandB esperado 4, obtenido {b}"
    assert tens == 1 and ones == 3, f"suma esperada 13, obtenida {tens}{ones}"

    # Overflow circular de A: 9 -> 0
    await pulse_button(dut, 0)

    a, b = decode_operands(dut.uio_out.value)
    tens, ones = decode_outputs(dut.uo_out.value)

    assert a == 0, f"operandA esperado 0, obtenido {a}"
    assert b == 4, f"operandB esperado 4, obtenido {b}"
    assert tens == 0 and ones == 4, f"suma esperada 04, obtenida {tens}{ones}"

