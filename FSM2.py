"""
FSM Generator from decimal sequence with Excel documentation and VHDL code output
Author: Julian Marquez Gutierrez
Email: julianmarquezgtz@gmail.com
GitHub: https://github.com/julianmarquezgtz-eng
Date: 2025-07-07
"""
def validar_binario_8bits(b):
    return len(b) == 8 and all(c in '01' for c in b)

def validar_hex_16bits(h):
    try:
        return len(h) <= 4 and 0 <= int(h, 16) <= 0xFFFF
    except:
        return False

def validar_bin7bits(b):
    return len(b) == 7 and all(c in '01' for c in b)

def sufijo_prefijo(secuencia, prefijo_objetivo):
    for i in range(len(secuencia)):
        sufijo = secuencia[i:]
        if prefijo_objetivo.startswith(sufijo):
            return len(sufijo)
    return 0

def generar_transiciones(secuencia):
    estados = [chr(ord('A') + i) for i in range(len(secuencia))]
    transiciones = {e: {} for e in estados}
    estados.append('A')  # Estado reinicio

    for i, estado in enumerate(estados[:-1]):
        bit_esperado = secuencia[i]

        for bit_recibido in ['0', '1']:
            if bit_recibido == bit_esperado:
                sig_estado = estados[i+1] if i+1 < len(secuencia) else 'A'
            else:
                sec_parcial = secuencia[:i] + bit_recibido
                l = sufijo_prefijo(sec_parcial, secuencia)
                sig_estado = estados[l] if l < len(estados) else 'A'

            transiciones[estado][bit_recibido] = sig_estado

    return transiciones

# Solicitar secuencia
print("Introduce un número decimal entre 0 y 255 (será convertido a binario de 8 bits):")
while True:
    try:
        num = int(input(">> ").strip())
        if 0 <= num <= 255:
            secuencia = f"{num:08b}"
            print(f"Secuencia binaria generada: {secuencia}")
            break
        else:
            print("Número fuera de rango. Debe estar entre 0 y 255.")
    except ValueError:
        print("Entrada inválida. Debe ser un número entero.")


estados = [chr(ord('A') + i) for i in range(len(secuencia))]

print("\nIntroduce valores HEXADECIMALES de 16 bits (hasta 4 dígitos hex) para cada estado:")
hex_estados = []
for est in estados:
    while True:
        h = input(f"Estado {est} (hex): ").strip().upper()
        if validar_hex_16bits(h):
            hex_estados.append(h.zfill(4))
            break
        print("Hex inválido. Debe tener hasta 4 dígitos hexadecimales (ej: F3C0).")

print("\nIntroduce valores BINARIOS de 7 bits para contador (0 a 3):")
cont_bin = []
for i in range(4):
    while True:
        b = input(f"Contador {i}: ").strip()
        if validar_bin7bits(b):
            cont_bin.append(b)
            break
        print("Binario inválido. Debe tener exactamente 7 bits (ej: 0000001).")

transiciones = generar_transiciones(secuencia)

with open("FSM_generada.vhd", "w") as f:
    f.write(f"""library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity FSM is
    port (
        clk, x : in std_logic;
        y, clkout : out std_logic;
        DE : out std_logic_vector(15 downto 0);
        DC : out std_logic_vector(6 downto 0)
    );
end entity;

architecture behavior of FSM is
    type estados is ({', '.join(estados)});
    signal edo_act, edo_sig, edo_ant : estados := A;
    signal cont : integer range 0 to 3 := 0;
    signal y_int : std_logic := '0';
begin
    clkout <= not clk;
    y <= y_int;

    process (x, edo_act)
    begin
        case edo_act is
""")
    for est in estados:
        f.write(f"            when {est} =>\n")
        idx = ord(est) - ord('A')
        f.write(f"                DE <= X\"{hex_estados[idx]}\";\n")
        f.write("                if x = '0' then\n")
        sig_0 = transiciones[est]['0']
        f.write(f"                    edo_sig <= {sig_0};\n")
        if est == estados[-1] and secuencia[-1] == '0':
            f.write("                    y_int <= '1';\n")
        else:
            f.write("                    y_int <= '0';\n")
        f.write("                elsif x = '1' then\n")
        sig_1 = transiciones[est]['1']
        f.write(f"                    edo_sig <= {sig_1};\n")
        if est == estados[-1] and secuencia[-1] == '1':
            f.write("                    y_int <= '1';\n")
        else:
            f.write("                    y_int <= '0';\n")
        f.write("                else\n")
        f.write("                    edo_sig <= " + est + ";  -- Mantener estado si bit inválido\n")
        f.write("                    y_int <= '0';\n")
        f.write("                end if;\n\n")

    f.write(f"""        end case;
    end process;

    process (cont)
    begin
        case cont is
            when 0 => DC <= "{cont_bin[0]}";
            when 1 => DC <= "{cont_bin[1]}";
            when 2 => DC <= "{cont_bin[2]}";
            when 3 => DC <= "{cont_bin[3]}";
            when others => DC <= "1111111";
        end case;
    end process;

    process (clk)
    begin
        if rising_edge(clk) then
            edo_ant <= edo_act;
            edo_act <= edo_sig;

            if edo_ant = {estados[-1]} and edo_act = A and x = '{secuencia[-1]}' then
                if cont < 3 then
                    cont <= cont + 1;
                else
                    cont <= 0;
                end if;
            end if;
        end if;
    end process;

end architecture;
""")

print("\n Archivo FSM_generada.vhd generado con éxito.")

from openpyxl import Workbook

# Función para encontrar el estado al que retrocede en caso de error
def calcular_estado_retroceso(subcadena):
    for i in range(len(subcadena), 0, -1):
        if secuencia.startswith(subcadena[-i:]):
            return chr(ord('A') + i)
    return "A"

# Crear el archivo Excel
wb = Workbook()
ws = wb.active
ws.title = "Tabla de Estados"

# Encabezado con la secuencia
ws.append(["Secuencia Binaria:", secuencia])
ws.append(["Valor Decimal:", int(secuencia, 2)])
ws.append([])  # Línea en blanco
ws.append(["Estado Actual", "Entrada (x)", "Siguiente Estado", "Salida (y)"])

for i in range(len(estados)):
    estado_actual = estados[i]
    x_esperado = secuencia[i]

    for x in ["0", "1"]:
        if x == x_esperado:
            siguiente_estado = estados[i+1] if i < len(estados) - 1 else "A"
            y_salida = "1" if i == len(estados) - 1 else "0"
        else:
            secuencia_parcial = secuencia[:i] + x
            retroceso = calcular_estado_retroceso(secuencia_parcial)
            siguiente_estado = retroceso
            y_salida = "0"
        ws.append([estado_actual, x, siguiente_estado, y_salida])

# Guardar el archivo
wb.save("FSM_estados.xlsx")

print(" Archivo FSM_estados.xlsx generado con éxito.")
