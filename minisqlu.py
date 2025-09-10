import re

# Expresiones regulares para validar códigos
regex_estudiante = re.compile(r"^202[0-9]-[0-9]{5}$")
regex_curso = re.compile(r"^[A-Z]{3}[0-9]{3}$")

def validar_linea(linea):
    linea = linea.split('#')[0].strip()  # Quitar comentarios y espacios
    if not linea:
        return None  # Línea vacía o comentario

    # Separar tokens, considerando que ; es un token separado
    tokens = []
    temp = ""
    for c in linea:
        if c == ';':
            if temp:
                tokens.append(temp)
                temp = ""
            tokens.append(';')
        elif c.isspace():
            if temp:
                tokens.append(temp)
                temp = ""
        else:
            temp += c
    if temp:
        tokens.append(temp)

    # Validar estructura básica
    if len(tokens) < 3:
        return "Error: instrucción incompleta"

    comando = tokens[0]
    tipo = tokens[1]

    if comando == "INSERT":
        if len(tokens) != 5 or tokens[-1] != ';':
            return "Error: sintaxis incorrecta en INSERT"
        nombre = tokens[2]
        codigo = tokens[3]

        if tipo == "estudiante":
            if not nombre.isalpha():
                return f"Error: nombre de estudiante inválido ({nombre})"
            if not regex_estudiante.match(codigo):
                return f"Error: código de estudiante inválido ({codigo})"
        elif tipo == "curso":
            if not nombre.isalpha():
                return f"Error: nombre de curso inválido ({nombre})"
            if not regex_curso.match(codigo):
                return f"Error: código de curso inválido ({codigo})"
        else:
            return f"Error: tipo inválido ({tipo})"

    elif comando == "SHOW":
        if len(tokens) != 4 or tokens[-1] != ';':
            return "Error: sintaxis incorrecta en SHOW"
        dato = tokens[2]
        if tipo == "estudiante":
            if not dato.isalpha():
                return f"Error: nombre de estudiante inválido ({dato})"
        elif tipo == "curso":
            if not regex_curso.match(dato):
                return f"Error: código de curso inválido ({dato})"
        else:
            return f"Error: tipo inválido ({tipo})"
    else:
        return f"Error: comando inválido ({comando})"

    return "Instrucción válida: ejecutada"

def main():
    try:
        with open("programa.txt", "r", encoding="utf-8") as f:
            for linea in f:
                resultado = validar_linea(linea)
                if resultado:
                    print(resultado)
    except FileNotFoundError:
        print("Error: no se encontró el archivo programa.txt")

if __name__ == "__main__":
    main()
