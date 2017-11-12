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

output = []

def p_output(p):
    'output : statement'
    output.append(p[1]['text'])
    print('Parser outpu:\n')
    print(p[1]['text'])

def p_statement(p):
    '''
    statement : hash_stmt
                | join_stmt
                | sort_stmt
                | materialize_stmt
                | limit_stmt

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
                | seq_scan condition
    '''
    seq_scan = p[1]
    table_name = seq_scan['table_name']
    text = '''Performing sequential scan on table "{}"'''.format(table_name)
    if (len(p) == 3):
        condition = p[2]
        text += ' with condition {}'.format(condition)
    summary = seq_scan['summary']
    text += '. {}'.format(summary)
    p[0] = {}
    p[0]['text'] = text
    p[0]['table_name'] = table_name

def p_index_scan_stmt(p):
    '''
    index_scan_stmt : index_scan
                | index_scan condition
    '''
    index_scan = p[1]
    table_name = index_scan['table_name']
    index = index_scan['index']
    text = 'Performing index scan on table "{}" using index "{}"'.format(table_name, index)
    if (len(p) == 3):
        condition = p[2]
        text += ' with condition {}'.format(condition)
    summary = index_scan['summary']
    text += '. {}'.format(summary)
    p[0] = {}
    p[0]['text'] = text
    p[0]['table_name'] = table_name

def p_index_only_scan_stmt(p):
    '''
    index_only_scan_stmt : index_only_scan
                    | index_only_scan condition
    '''
    index_scan = p[1]
    table_name = index_scan['table_name']
    index = index_scan['index']
    text = 'Performing index scan on table "{}" using only index "{}"'.format(table_name, index)
    if (len(p) == 3):
        condition = p[2]
        text += ' with condition {}'.format(condition)
    summary = index_scan['summary']
    text += '. {}'.format(summary)
    p[0] = {}
    p[0]['text'] = text
    p[0]['table_name'] = table_name

def p_bmp_scan_stmt(p):
    '''
    bmp_scan_stmt : bmp_heap_scan_stmt 
                | bmp_heap_scan_stmt SUBOPS bmp_scan_stmt_tail
    '''
    heap_scan = p[1]
    text = p[1]['text']
    if (len(p) == 4):
        tail_stmt = p[3]
        text = '{} {}'.format(p[3]['text'], text)
    p[0] = {}
    p[0]['text'] = text

def p_bmp_scan_stmt_tail(p):
    'bmp_scan_stmt_tail : bmp_index_scan_stmt'
    p[0] = p[1]

def p_bmp_heap_scan_stmt(p):
    '''
    bmp_heap_scan_stmt : bmp_heap_scan 
                    | bmp_heap_scan condition
    '''
    heap_scan = p[1]
    table_name = heap_scan['table_name']
    text = '''Performing bitmap heap scan on table "{}"'''.format(table_name)
    if (len(p) == 3):
        condition = p[2]
        text += ' with condition {}'.format(condition)
    summary = heap_scan['summary']
    text += '. {}'.format(summary)
    p[0] = {}
    p[0]['text'] = text
    p[0]['table_name'] = table_name

def p_bmp_index_scan_stmt(p):
    '''
    bmp_index_scan_stmt : bmp_index_scan 
                    | bmp_index_scan condition
    '''
    index_scan = p[1]
    table_name = index_scan['table_name']
    text = '''Performing bitmap index scan on table "{}"'''.format(table_name)
    if (len(p) == 3):
        condition = p[2]
        text += ' with condition {}'.format(condition)
    summary = index_scan['summary']
    text += '. {}'.format(summary)
    p[0] = {}
    p[0]['text'] = text
    p[0]['table_name'] = table_name

def p_nested_join_stmt(p):
    '''
    nested_join_stmt : nested_loop SUBOPS statement SUBOPS statement
    '''
    join_summary = p[1]
    outer_stmt = p[3]
    outer_table_name = outer_stmt['table_name']
    outer_table_text = outer_stmt['text']
    inner_stmt = p[5]
    inner_table_name = inner_stmt['table_name']
    inner_table_text = inner_stmt['text']
    text = 'First, scan the outer table "{}". {} Then, scan the inner table "{}". {} Perfoming nested loop join on table "{}" and table "{}". {}'.format(outer_table_name, outer_table_text, inner_table_name, inner_table_text, outer_table_name, inner_table_name, join_summary)
    p[0] = {}
    p[0]['text'] = text

def p_hash_join_stmt(p):
    'hash_join_stmt : hash_join condition SUBOPS statement SUBOPS statement'
    join_summary = p[1]
    condition = p[2]
    outer_stmt = p[4]
    outer_table_name = outer_stmt['table_name']
    outer_table_text = outer_stmt['text']
    inner_stmt = p[6]
    inner_table_name = inner_stmt['table_name']
    inner_table_text = inner_stmt['text']
    text = 'First, scan the outer table "{}". {} Then, scan the inner table "{}". {} Perfoming hash join on table "{}" and table "{}" with condition "{}". {}'.format(outer_table_name, outer_table_text, inner_table_name, inner_table_text, outer_table_name, inner_table_name, condition, join_summary)
    p[0] = {}
    p[0]['text'] = text

def p_hash_stmt(p):
    '''
    hash_stmt : hash SUBOPS scan_stmt
                | scan_stmt
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else:
        sub_text = p[3]['text']
        hash_summary = p[1]
        p[0] = p[3]
        p[0]['text'] = '{} Then perform hashing on the previous output.  {}'.format(sub_text, hash_summary)

def p_merge_join_stmt(p):
    'merge_join_stmt : merge_join condition SUBOPS statement SUBOPS statement'
    join_summary = p[1]
    condition = p[2]
    outer_stmt = p[4]
    outer_table_name = outer_stmt['table_name']
    outer_table_text = outer_stmt['text']
    inner_stmt = p[6]
    inner_table_name = inner_stmt['table_name']
    inner_table_text = inner_stmt['text']
    text = 'First, sort the outer table "{}". {} Then, sort the inner table "{}". {} Perfoming merge join on table "{}" and table "{}" with condition "{}". {}'.format(outer_table_name, outer_table_text, inner_table_name, inner_table_text, outer_table_name, inner_table_name, condition, join_summary)
    p[0] = {}
    p[0]['text'] = text

def p_sort_stmt(p):
    'sort_stmt : sort sort_key SUBOPS statement'
    sort_summary = p[1]
    sort_key = p[2]
    sub_stmt = p[4]
    table_name = sub_stmt['table_name']
    sub_text = sub_stmt['text']
    text = '{} After that, sort the output by {}. {}'.format(sub_text, sort_key, sort_summary)
    p[0] = {}
    p[0]['text'] = text
    p[0]['table_name'] = table_name

def p_materialize_stmt(p):
    'materialize_stmt : materialize SUBOPS statement'
    materialize_summary = p[1]
    sub_text = p[3]['text']
    p[0] = p[3]
    p[0]['text'] = '{} Save output of the previous query to the secondary disk. {}'.format(sub_text, materialize_summary)

def p_limit_stmt(p):
    'limit_stmt : limit SUBOPS statement'
    limit_summary = p[1]
    sub_text = p[3]['text']
    p[0] = p[3]
    p[0]['text'] = '{} From the output of the previous operation, limit the number of rows returned according to the given query. {}'.format(sub_text, limit_summary)

def p_seq_scan(p):
    'seq_scan : SEQUENTIAL SCAN ON table summary'
    table_name = p[4]
    summary = p[5]
    p[0] = {}
    p[0]['table_name'] = table_name
    p[0]['summary'] = summary

def p_index_scan(p):
    'index_scan : INDEX SCAN index ON table summary'
    index = p[3]
    table_name = p[5]
    summary = p[6]
    p[0] = {}
    p[0]['index'] = index
    p[0]['table_name'] = table_name
    p[0]['summary'] = summary

def p_index_only_scan(p):
    'index_only_scan : INDEX ONLY SCAN index ON table summary'
    index = p[4]
    table_name = p[6]
    summary = p[7]
    p[0] = {}
    p[0]['index'] = index
    p[0]['table_name'] = table_name
    p[0]['summary'] = summary

def p_bmp_heap_scan(p):
    'bmp_heap_scan : BITMAP HEAP SCAN ON table summary'
    table_name = p[5]
    summary = p[6]
    p[0] = {}
    p[0]['table_name'] = table_name
    p[0]['summary'] = summary

def p_bmp_index_scan(p):
    'bmp_index_scan : BITMAP INDEX SCAN ON table summary'
    table_name = p[5]
    summary = p[6]
    p[0] = {}
    p[0]['table_name'] = table_name
    p[0]['summary'] = summary

def p_condition(p):
    '''
    condition : filter
            | index_cond
            | recheck
            | merge_cond
            | hash_cond
    '''
    p[0] = p[1]

def p_filter(p):
    'filter : FILTER COLON predicate'
    p[0] = p[3]

def p_index_cond(p):
    'index_cond : INDEX CONDITION COLON predicate'
    p[0] = p[4]

def p_recheck(p):
    'recheck : RECHECK CONDITION COLON predicate'
    p[0] = p[4]

def p_summary(p):
    'summary : LPAREN COST EQ COST_VAL TO COST_VAL ROWS EQ INT WIDTH EQ INT RPAREN'
    startup_cost = p[4]
    final_cost = p[6]
    rows = p[9]
    width = p[12]
    p[0] = '''This operation took {} miliseconds to initialize, {} miliseconds to complete, returning {} rows and {} columns.'''.format(startup_cost, final_cost, rows, width)

def p_predicate(p):
    '''
    predicate : field ops field
                | LPAREN predicate RPAREN
                | predicate AND predicate
                | predicate OR predicate
    '''
    p[0] = '{} {} {}'.format(p[1], p[2], p[3])

def p_ops(p):
    '''
    ops : EQ
        | GE
        | LE
        | GT
        | LT
        | NE
    '''
    if (p[1] == '='):
        p[0] = 'equal'
    elif (p[1] == '>='):
        p[0] = 'greater than or equal'
    elif (p[1] == '<='):
        p[0] = 'less than or equal'
    elif (p[1] == '>'):
        p[0] = 'greater than'
    elif (p[1] == '<'):
        p[0] = 'less than'
    else:
        p[0] = 'not equal'

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
            | INT TYPE ID
    '''
    literals = p[1]
    type_class = p[3]
    p[0] = '{} of type {}'.format(literals, type_class)

def p_attribute(p):
    '''
    attribute : table IN ID
            | ID
    '''
    if (len(p) == 4):
        p[0] = '{} in {}'.format(p[3], p[1])
    else:
        p[0] = p[1]

def p_nested_loop(p):
    'nested_loop : NESTED LOOP summary'
    p[0] = p[3]

def p_materialize(p):
    'materialize : MATERIALIZE summary'
    p[0] = p[2]

def p_limit(p):
    'limit : LIMIT summary'
    p[0] = p[2]

def p_hash_join(p):
    'hash_join : HASH JOIN summary'
    p[0] = p[3]

def p_hash(p):
    'hash : HASH summary'
    p[0] = p[2]

def p_merge_join(p):
    'merge_join : MERGE JOIN summary'
    p[0] = p[3]

def p_merge_cond(p):
    'merge_cond : MERGE CONDITION COLON predicate'
    p[0] = p[4]

def p_sort(p):
    'sort : SORT summary'
    p[0] = p[2]

def p_sort_key(p):
    'sort_key : SORT KEY COLON attribute'
    p[0] = p[4]

def p_hash_cond(p):
    'hash_cond : HASH CONDITION COLON predicate'
    p[0] = p[4]

def p_table(p):
    '''
    table : ID
        | ID ID
    '''
    table_name = p[1]
    if (len(p) == 3):
        alias = p[2]
        p[0] = '{} as {}'.format(table_name, alias)
    else:
        p[0] = table_name

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

def parse(s):
    output.clear()
    parser.parse(s)
    return output[0]

#while 1:
#    try:
#        s = input('qplex > ')
#    except EOFError:
#        break
#    parser.parse(s)
