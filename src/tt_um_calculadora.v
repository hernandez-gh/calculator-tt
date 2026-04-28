/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none
module tt_um_calculadora (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // Botones en ui_in[0] y ui_in[1]
    // Sincronizador de 2 etapas
    reg btnA_sync0, btnA_sync1;
    reg btnB_sync0, btnB_sync1;

    always @(posedge clk) begin
        btnA_sync0 <= ui_in[0];
        btnA_sync1 <= btnA_sync0;

        btnB_sync0 <= ui_in[1];
        btnB_sync1 <= btnB_sync0;
    end

    // Detector de flanco
    reg btnA_prev, btnB_prev;

    wire btnA_rise = btnA_sync1 & ~btnA_prev;
    wire btnB_rise = btnB_sync1 & ~btnB_prev;

    always @(posedge clk) begin
        if (!rst_n) begin
            btnA_prev <= 1'b0;
            btnB_prev <= 1'b0;
        end else begin
            btnA_prev <= btnA_sync1;
            btnB_prev <= btnB_sync1;
        end
    end

    // Registros de operandos
    reg [3:0] operandA;
    reg [3:0] operandB;

    always @(posedge clk) begin
        if (!rst_n) begin
            operandA <= 4'd0;
            operandB <= 4'd0;
        end else if (ena) begin
            if (btnA_rise) begin
                if (operandA == 4'd9)
                    operandA <= 4'd0;
                else
                    operandA <= operandA + 4'd1;
            end

            if (btnB_rise) begin
                if (operandB == 4'd9)
                    operandB <= 4'd0;
                else
                    operandB <= operandB + 4'd1;
            end
        end
    end

    // Suma
    wire [4:0] sum;
    assign sum = operandA + operandB;

    // Conversión a decenas y unidades
    reg [3:0] tens;
    reg [3:0] ones;

    wire [4:0] sum_minus_10;
    assign sum_minus_10 = sum - 5'd10;

    always @(*) begin
        if (sum < 5'd10) begin
            tens = 4'd0;
            ones = sum[3:0];
        end else begin
            tens = 4'd1;
            ones = sum_minus_10[3:0];
        end
    end

    // Salidas
    // uo_out[3:0] = unidades
    // uo_out[7:4] = decenas
    assign uo_out = {tens, ones};

    // Debug:
    // uio_out[3:0] = operandA
    // uio_out[7:4] = operandB
    assign uio_out = {operandB, operandA};
    assign uio_oe  = 8'hFF;

    wire _unused = &{uio_in, ui_in[7:2], 1'b0};
  

endmodule

