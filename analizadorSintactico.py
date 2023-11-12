from ply import lex, yacc

errores_sintacticos = []

reserved = {
    'include': 'INCLUDE',
    'iostream': 'IOSTREAM',
    'int': 'INT',
    'main': 'MAIN',
    'bool': 'BOOL',
    'char': 'CHAR',
    'long': 'LONG',
    'true': 'TRUE',
    'false': 'FALSE',
}

tokens = list(reserved.values()) + [
    'LBRACE', 'RBRACE', 'COMMENT', 'ID', 'EQUALS', 'NUMBER', 'PLUS', 'MINUS',
    'TIMES', 'DIVIDE', 'AND', 'OR', 'NOT', 'LPAREN', 'RPAREN', 'SEMICOLON',
    'SINGLE_QUOTE', 'LESS_THAN', 'GREATER_THAN', 'EQUALITY', 'INEQUALITY',
    'GREATER_THAN_OR_EQUAL', 'LESS_THAN_OR_EQUAL'
]

# Expresión regular para comentarios de una línea
t_COMMENT = r'\/\/.*'

t_INCLUDE = r'\#include'
t_IOSTREAM = r'\<iostream\>'
t_INT = r'int'
t_MAIN = r'main'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQUALS = r'='
t_NUMBER = r'\d+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_BOOL = r'bool'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_CHAR = r'char'
t_LONG = r'long'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_SINGLE_QUOTE = r'\''
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_EQUALITY = r'=='
t_INEQUALITY = r'!='
t_GREATER_THAN_OR_EQUAL = r'>='
t_LESS_THAN_OR_EQUAL = r'<='

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verificar si es una palabra clave
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Carácter no permitido '%s'" % t.value[0])
    t.lexer.skip(1)
    

lexer = lex.lex()

def p_main_function(p):
    'main_function : INCLUDE IOSTREAM INT MAIN LPAREN RPAREN LBRACE code RBRACE'
    p[0] = p[5]

def p_code(p):
    '''code : statement
            | code statement
            | empty'''

def p_statement(p):
    '''statement : COMMENT
                 | declaration
                 | assignment'''
    p[0] = None

def p_declaration(p):
    '''declaration : simple_declaration
                   | long_declaration
                   | bool_declaration
                   | char_single_quote_declaration'''

def p_simple_declaration(p):
    '''simple_declaration : INT ID EQUALS expression SEMICOLON'''

def p_long_declaration(p):
    '''long_declaration : LONG ID EQUALS NUMBER SEMICOLON
                       | LONG INT ID EQUALS NUMBER SEMICOLON'''

def p_bool_declaration(p):
    '''bool_declaration : BOOL ID EQUALS expression SEMICOLON
                       | BOOL ID EQUALS BOOL_VALUE SEMICOLON'''

def p_char_single_quote_declaration(p):
    '''char_single_quote_declaration : CHAR ID EQUALS SINGLE_QUOTE ID SINGLE_QUOTE SEMICOLON'''

# Regla para las asignaciones
def p_assignment(p):
    '''assignment : simple_assignment
                  | complex_assignment
                  | not_assignment'''

def p_simple_assignment(p):
    '''simple_assignment : ID EQUALS expression SEMICOLON'''

def p_complex_assignment(p):
    '''complex_assignment : ID EQUALS LPAREN expression RPAREN SEMICOLON'''

def p_not_assignment(p):
    '''not_assignment : ID EQUALS NOT expression SEMICOLON'''

# Regla para expresiones
def p_expression(p):
    '''expression : ID PLUS ID
                  | ID MINUS ID
                  | ID TIMES ID
                  | ID DIVIDE ID
                  | ID EQUALS ID
                  | ID NOT ID
                  | ID AND ID
                  | ID OR ID
                  | ID EQUALITY ID
                  | ID INEQUALITY ID
                  | ID GREATER_THAN ID
                  | ID LESS_THAN ID
                  | ID GREATER_THAN_OR_EQUAL ID
                  | ID LESS_THAN_OR_EQUAL ID
                  | NUMBER
                  | LPAREN expression RPAREN
                  | NOT expression
                  | MINUS expression
                  | ID'''
    p[0] = None

# Regla para expresiones booleanas
def p_bool_expression(p):
    '''bool_expression : ID EQUALS ID
                       | ID NOT ID
                       | ID AND ID
                       | ID OR ID
                       | ID EQUALITY ID
                       | ID INEQUALITY ID
                       | ID GREATER_THAN ID
                       | ID LESS_THAN ID
                       | ID GREATER_THAN_OR_EQUAL ID
                       | ID LESS_THAN_OR_EQUAL ID
                       | LPAREN bool_expression RPAREN'''
    p[0] = None

# Regla para valores booleanos
def p_bool_value(p):
    '''BOOL_VALUE : TRUE
                  | FALSE'''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    global errores_sintacticos
    if p:
        estado = "** Error de sintaxis en la línea: {:4} Posición: {:4} Token inesperado: {:16}".format(str(p.lineno), str(p.lexpos), str(p.value))
        errores_sintacticos.append(estado)
        with open('erroresSintacticos.txt', 'a') as error_file:
            error_file.write(estado + '\n')
        p.lexer.skip(1)
    else:
        print("Error de sintaxis: Fin inesperado del input")

parser = yacc.yacc()

def parse(program):
    lexer.input(program)
    parser.parse(program)
    if not errores_sintacticos:
        print("No se detectaron errores sintácticos.")
    else:
        print("Errores sintácticos encontrados. Consulta el archivo 'erroresSintacticos.txt' para más detalles.")


file = open('codigocpp.txt')
codigo = file.read()
file.close()
parse(codigo)