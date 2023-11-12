from ply import lex, yacc

# Definición de los tokens
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'ID',
    'INT',
    'BOOL',
    'CHAR',
    'LONG',
    'AND',
    'OR',
    'NOT',
    'EQUALTO',
    'NOTEQUAL',
    'GREATERTHAN',
    'LESSTHAN',
    'POUND',
    'SQUOTE',
)

# Expresiones regulares para los tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMICOLON = r';'
t_INT     = r'int'
t_BOOL    = r'bool'
t_CHAR    = r'char'
t_LONG    = r'long'
t_AND     = r'&&'
t_OR      = r'\|\|'
t_NOT     = r'!'
t_EQUALTO = r'=='
t_NOTEQUAL = r'!='
t_GREATERTHAN = r'>'
t_LESSTHAN = r'<'
t_POUND   = r'\#'
t_SQUOTE  = r'\''

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios y tabulaciones
t_ignore  = ' \t'

# Ignorar las líneas que comienzan con '#'
def t_preprocessor(t):
    r'\#.*'
    pass

# Manejo de errores
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Tabla de símbolos
symbol_table = {}

# Definición de la gramática
def p_program(p):
    'program : declaration_list'
    p[0] = p[1]

def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaration(p):
    'declaration : type_specifier ID SEMICOLON'
    symbol_table[p[2]] = p[1]
    p[0] = (p[1], p[2])

def p_type_specifier(p):
    '''type_specifier : INT
                      | BOOL
                      | CHAR
                      | LONG'''
    p[0] = p[1]

# Manejo de errores
def p_error(p):
    with open('erroresSemanticos.txt', 'a') as f:
        estado = "** Error de sintaxis en la línea: {:4} Posición: {:4} Token inesperado: {:16}".format(str(p.lineno), str(p.lexpos), str(p.value))
        f.write(estado + '\n')

# Construir el parser
parser = yacc.yacc()

# Prueba del analizador semántico
with open('codigocpp.txt', 'r') as f:
    s = f.read()
    result = parser.parse(s)