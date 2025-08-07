# FSM Generator from Decimal Sequence

This project generates a Finite State Machine (FSM) based on a user-input decimal sequence (0-255), converted into an 8-bit binary sequence.

## Features

- Validates inputs for decimal numbers, 16-bit hexadecimal codes, and 7-bit binary counters.
- Generates FSM transitions according to the input sequence.
- Produces a detailed Excel spreadsheet (`FSM_estados.xlsx`) describing states, inputs, outputs, and transitions.
- Outputs ready-to-use VHDL code (`FSM_generada.vhd`) for FPGA or hardware implementation.
- Uses hexadecimal codes to drive a 16-segment display representing states.
- Counts cycles with a 7-segment display.

## Usage

1. Run the Python script.
2. Input a decimal number between 0 and 255.
3. Provide 16-bit hexadecimal codes for each FSM state.
4. Provide 7-bit binary codes for cycle counters (0 to 3).
5. The script will generate:
   - `FSM_estados.xlsx`: Excel documentation of FSM states and transitions.
   - `FSM_generada.vhd`: VHDL code implementing the FSM.

## Requirements

- Python 3.x
- `openpyxl` library (`pip install openpyxl`)

## Author

Julián Márquez Gutiérrez
Email: julianmarquezgtz@gmail.com  
GitHub: julianmarquezgtz-eng (https://github.com/julianmarquezgtz-eng)
