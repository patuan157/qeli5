reserved = {
        # Onetime
        'Result': 'RESULT',
        'One-Time': 'ONE_TIME',
        # Intersect
        'HashSetOp': 'HASH_SET_OP',
        'Intersect': 'INTERSECT',
        'All': 'ALL',
        # Union
        'Unique': 'UNIQUE',
        'Append': 'APPEND',
        # Aggregate
        'Aggregate': 'AGGREGATE'
        # Limit
        'Limit': 'LIMIT',
        # Join
        'Nested': 'NESTED',
        'Loop': 'LOOP',
        'Merge': 'MERGE',
        'Hash': 'HASH',
        'Join': 'JOIN',
        # Sort/Order By
        'Sort': 'SORT',
        'Key': 'KEY',
        # Group By
        'HashAggregate': 'HASH_AGG'
        'Group': 'GROUP',
        'BitmapAnd': 'BMP_AND',
        # Scan
        'Bitmap': 'BITMAP',
        'Seq': 'SEQUENTIAL',
        'Heap': 'HEAP',
        'Index': 'INDEX',
        'Subquery': 'SUBQUERY',
        'Only': 'ONLY',
        'Scan': 'SCAN',
        'Materialize': 'MATERIALIZE',
        # Condition
        'Recheck': 'RECHECK',
        'Filter': 'FILTER',
        'Cond': 'CONDITION',
        'using': 'USING',
        # Operator
        '<>': 'NOT_EQUAL',
        '<=': 'LE',
        '>=': 'GE',
        'AND': 'AND',
        'OR': 'OR',
        # Keywords
        'on': 'ON',
        'cost': 'COST',
        'rows': 'ROWS',
        'width': 'WIDTH',
}

tokens = [
        # KEYWORDS
        'LPAREN',
        'RPAREN',
        'COLON',
        'TO',

        # OPERATORS
        'EQUAL',
        'LT',
        'GT',
        
        # REGEX
        'ID',
        'COST_VAL',
        'INT',
        'LITERALS'
] + list(reserved.values())

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COLON     = r'\:'
t_TO        = r'\.\.'
t_EQUAL     = r'='
t_LT        = r'<'
t_GT        = r'>'
t_LITERALS  = r'\'(\.|[^\'])*\''

def t_ID(t):
    r'[A-z][A-z_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COST_VAL(t):
    r'([1-9]\d*|0)\.\d{2}'
    try:
        t.value = float(t.value)
    except:
        print('Float value too large %f', t.value)
        t.value = 0
    return t

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except:
        print('Integer value too large %d', t.value)
        t.value = 0
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

while True:
    string = input()
    lexer.input(string)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

names = {}

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression'''
    if (p[2] == '+'):
        p[0] = p[1] + p[3]
    elif (p[2] == '-'):
        p[0] = p[1] - p[3]
    elif (p[2] == '*'):
        p[0] = p[1] * p[3]
    elif (p[2] == '/'):
        p[0] = p[1] / p[3]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print('Undefined name "%s"' % p[1])
        p[0] = 0

def p_error(p):
    print('Syntax error at "%s"' % p.value)

import ply.yacc as yacc
parser = yacc.yacc()

while 1:
    try:
        s = input('cal > ')
    except EOFError:
        break
    parser.parse(s)
