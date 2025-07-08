from colorama import Fore

def input_entero(msg):
    while True:
        entrada = input(msg).strip()
        if not entrada:
            print(Fore.RED + "Por favor, no deje el campo vacío.")
            continue
        try:
            return int(entrada)
        except ValueError:
            print(Fore.RED + "Por favor, ingrese un número entero.")

def input_float(msg):
    while True:
        entrada = input(msg).strip()
        if not entrada:
            print(Fore.RED + "Por favor, no deje el campo vacío.")
            continue
        try:
            return float(entrada)
        except ValueError:
            print(Fore.RED + "Por favor, ingrese un número válido.")

def input_string(msg):
    while True:
        valor = input(msg).strip()
        if not valor:
            print(Fore.RED + "Por favor, ingrese un texto que no esté vacío.")
            continue
        if valor.isdigit():
            print(Fore.RED + "El texto no puede ser solo números.")
            continue
        return valor
