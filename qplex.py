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
        'Aggregate': 'AGGREGATE',
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
        'HashAggregate': 'HASH_AGG',
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
        'SUBOPS',
        'LPAREN',
        'RPAREN',
        'TYPE',
        'COLON',
        'TO',
        'IN',

        # OPERATORS
        'NE',
        'GE',
        'LE',
        'EQ',
        'LT',
        'GT',
        
        # REGEX
        'ID',
        'COST_VAL',
        'INT',
        'LITERALS'
] + list(reserved.values())

t_SUBOPS    = r'->'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_TYPE      = r'\:\:'
t_COLON     = r'\:'
t_TO        = r'\.\.'
t_IN        = r'\.'
t_NE        = r'<>'
t_LE        = r'<='
t_GE        = r'>='
t_EQ        = r'='
t_LT        = r'<'
t_GT        = r'>'
t_LITERALS  = r'\'(\.|[^\'])*\''

def t_ID(t):
    r'[A-z][A-z0-9_]*'
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

#while True:
#    print('=======================')
#    print('\n')
#    string = input()
#    lexer.input(string)
#    while True:
#        tok = lexer.token()
#        if not tok:
#            break
#        print(tok)

precedence = (
    ('nonassoc', 'SUBOPS'),
    ('left', 'OR'),
    ('left', 'AND'),
)

def p_statement(p):
    '''
    statement : scan_stmt
                | join_stmt
                | sort_stmt

                | filter
                | index_cond
                | recheck
                | summary
                | predicate
                | field
                | empty
    '''
    p[0] = p[1]

def p_scan_stmt(p):
    '''
    scan_stmt : seq_scan_stmt
                | index_scan_stmt
                | index_only_scan_stmt
                | bmp_scan_stmt
    '''
    p[0] = p[1]

def p_join_stmt(p):
    '''
    join_stmt : nested_join_stmt
                | hash_join_stmt
                | merge_join_stmt
    '''
    p[0] = p[1]

def p_seq_scan_stmt(p):
    '''
    seq_scan_stmt : seq_scan
                | seq_scan filter
    '''
    print('Sequential Scan Statement')

def p_index_scan_stmt(p):
    '''
    index_scan_stmt : index_scan
                | index_scan index_cond
    '''
    print('Index Scan Statement')

def p_index_only_scan_stmt(p):
    '''
    index_only_scan_stmt : index_only_scan
                    | index_only_scan index_cond
    '''
    print('Index Only Scan Statement')

def p_bmp_scan_stmt(p):
    '''
    bmp_scan_stmt : bmp_heap_scan_stmt 
                | bmp_heap_scan_stmt SUBOPS bmp_scan_stmt_tail
    '''
    print('Bitmap Scan Statement')

def p_bmp_scan_stmt_tail(p):
    'bmp_scan_stmt_tail : bmp_index_scan_stmt'

def p_bmp_heap_scan_stmt(p):
    'bmp_heap_scan_stmt : bmp_heap_scan recheck'

def p_bmp_index_scan_stmt(p):
    '''
    bmp_index_scan_stmt : bmp_index_scan 
                    | bmp_index_scan index_cond
    '''

def p_nested_join_stmt(p):
    '''
    nested_join_stmt : nested_loop SUBOPS scan_stmt SUBOPS nested_join_stmt_tail
    '''
    print('Nested Loop Join')

def p_nested_join_stmt_tail(p):
    '''
    nested_join_stmt_tail : scan_stmt
                    | materialize SUBOPS scan_stmt
    '''

def p_hash_join_stmt(p):
    'hash_join_stmt : hash_join hash_cond hash_join_stmt_tail'
    print('Hash Join Statement')

def p_hash_join_stmt_tail(p):
    'hash_join_stmt_tail : SUBOPS scan_stmt SUBOPS hash_stmt'

def p_hash_stmt(p):
    'hash_stmt : hash SUBOPS scan_stmt'
    print('Hash Statement')

def p_merge_join_stmt(p):
    'merge_join_stmt : merge_join merge_cond merge_join_stmt_tail'
    print('Merge Join Statement')

def p_merge_join_stmt_tail(p):
    'merge_join_stmt_tail : SUBOPS sort_stmt SUBOPS sort_stmt'

def p_sort_stmt(p):
    'sort_stmt : sort sort_key SUBOPS statement'
    print('Sort Statement')

def p_seq_scan(p):
    'seq_scan : SEQUENTIAL SCAN ON table summary'
    p[0] = p[1]
    for i in range(2, len(p)):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_index_scan(p):
    'index_scan : INDEX SCAN USING index ON table summary'
    p[0] = p[1]
    for i in range(2, len(p)):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_index_only_scan(p):
    'index_only_scan : INDEX ONLY SCAN USING index ON table summary'
    p[0] = p[1]
    for i in range(2, len(p)):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_bmp_heap_scan(p):
    'bmp_heap_scan : BITMAP HEAP SCAN ON table summary'
    p[0] = p[1]
    for i in range(2, len(p)):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_bmp_index_scan(p):
    'bmp_index_scan : BITMAP INDEX SCAN ON table summary'
    p[0] = p[1]
    for i in range(2, len(p)):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_filter(p):
    'filter : FILTER COLON predicate'
    p[0] = p[1]
    for i in range(2, 4):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_index_cond(p):
    'index_cond : INDEX CONDITION COLON predicate'
    p[0] = p[1]
    for i in range(2, 5):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_recheck(p):
    'recheck : RECHECK CONDITION COLON predicate'
    p[0] = p[1]
    for i in range(2, 5):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_summary(p):
    'summary : LPAREN COST EQ COST_VAL TO COST_VAL ROWS EQ INT WIDTH EQ INT RPAREN'
    p[0] = p[1]
    for i in range(2, 14):
        p[0] += ',' + str(p[i])

def p_predicate(p):
    '''
    predicate : field ops field
                | LPAREN predicate RPAREN
                | predicate AND predicate
                | predicate OR predicate
    '''
    p[0] = p[1]
    for i in range(2, 4):
        p[0] += ',' + str(p[i])
    print(p[0])

def p_ops(p):
    '''
    ops : EQ
        | GE
        | LE
        | GT
        | LT
        | NE
    '''
    p[0] = p[1]

def p_field(p):
    '''
    field : INT
            | COST_VAL
            | value
            | attribute
    '''
    p[0] = p[1]

def p_value(p):
    '''
    value : LITERALS TYPE ID
    '''
    p[0] = '(' + str(p[3]) + ') ' + str(p[1])

def p_attribute(p):
    '''
    attribute : table IN ID
            | ID
    '''
    if (len(p) == 4):
        p[0] = str(p[1]) + '->' + str(p[3])
    else:
        p[0] = p[1]

def p_nested_loop(p):
    'nested_loop : NESTED LOOP summary'

def p_materialize(p):
    'materialize : MATERIALIZE summary'

def p_hash_join(p):
    'hash_join : HASH JOIN summary'

def p_hash(p):
    'hash : HASH summary'

def p_merge_join(p):
    'merge_join : MERGE JOIN summary'

def p_merge_cond(p):
    'merge_cond : MERGE CONDITION COLON predicate'

def p_sort(p):
    'sort : SORT summary'

def p_sort_key(p):
    'sort_key : SORT KEY COLON attribute'

def p_hash_cond(p):
    'hash_cond : HASH CONDITION COLON predicate'

def p_table(p):
    '''
    table : ID
        | ID alias
    '''
    p[0] = p[1]

def p_alias(p):
    'alias : ID'
    p[0] = p[1]

def p_index(p):
    'index : USING ID'
    p[0] = p[2]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print('Syntax error at "%s"' % p.value)

import ply.yacc as yacc
parser = yacc.yacc()

while 1:
    try:
        s = input('qplex > ')
    except EOFError:
        break
    parser.parse(s)
