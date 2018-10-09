`timescale 1ns/1ps

module toplevel ( input clk, output UART_TX, input UART_RX);
    assign UART_TX = UART_RX;
endmodule

