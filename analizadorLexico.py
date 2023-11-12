import ply.lex as lex

resultado_lexema = []
errores_lexicos = []

reservada = (
    'INCLUDE',
    'RETURN',
    'INT',
    'BOOL',
    'TRUE',
    'FALSE',
    'CHAR',
    'LONG',
)

tokens = reservada + (
    'ID',
    'ENTERO',
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'ASIGNAR',
    'PUNTOCOMA',
    'IGUALDAD',
    'DISTINTO',
    'MAYOR',
    'MENOR',
    'AND',
    'OR',
    'NOT',
    'COMILLA',
    'PARIZQ',
    'PARDER',
    'LLAVEIZQ',
    'LLAVEDER',
)

t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_ASIGNAR = r'='
t_PUNTOCOMA = ';'
t_IGUALDAD = r'=='
t_DISTINTO = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_COMILLA = r'\''
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'

def t_INCLUDE(t):
    r'\#include'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_INT(t):
    r'int'
    return t

def t_BOOL(t):
    r'bool'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_LONG(t):
    r'long'
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_coment_one(t):
    r'//.*\n'
    t.lexer.lineno += 1
    print('Comentario de una linea')

t_ignore = ' \t'

def t_error(t):
    global errores_lexicos
    estado = "** Token no valido en la linea: {:4} Lexema {:1} Posicion: {:4}".format(str(t.lineno), str(t.value), str(t.lexpos))
    errores_lexicos.append(estado)
    with open('erroresLexicos.txt', 'a') as error_file:
        error_file.write(estado + '\n')
    t.lexer.skip(1)

def funcionAnalizar(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)
    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        estado = "Linea: {:4} Tipo {:16} Lexema: {:16} Posicion {:4}".format(str(tok.lineno), str(tok.type), str(tok.value), str(tok.lexpos))
        resultado_lexema.append(estado)
        print(estado)
    if not errores_lexicos:
        print("No se detectaron errores léxicos.")
    else:
        print("Errores léxicos encontrados. Consulta el archivo 'erroresLexicos.txt' para más detalles.")
    return resultado_lexema

if __name__ == '__main__':
    file = open('codigocpp.txt')
    data = file.read()
    file.close()
    funcionAnalizar(data)