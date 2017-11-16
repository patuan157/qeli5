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
        'COMMA',
        'TO',
        'IN',

        # OPERATORS
        'MATCH',
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
        'LITERALS',
        'ALIAS',
] + list(reserved.values())

t_SUBOPS    = r'->'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_TYPE      = r'\:\:'
t_COLON     = r'\:'
t_COMMA     = r','
t_TO        = r'\.\.'
t_IN        = r'\.'
t_MATCH     = r'~~'
t_NE        = r'<>'
t_LE        = r'<='
t_GE        = r'>='
t_EQ        = r'='
t_LT        = r'<'
t_GT        = r'>'
t_LITERALS  = r'\'(\.|[^\'])*\''
t_ALIAS     = r'\"(\.|[^\"])*\"'

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
    print('Parser output:\n')
    # print(p[1]['text'])

def p_statement(p):
    '''
    statement : hash_stmt
                | join_stmt
                | sort_stmt
                | materialize_stmt
                | limit_stmt
                | append_stmt
                | aggregate_stmt
                | hashsetop_intersect_stmt
                | group_stmt
                | unique_stmt

                | empty
    '''
    p[0] = p[1]

def p_unique_stmt(p):
    '''
    unique_stmt : UNIQUE summary SUBOPS sort_stmt
    '''
    sub_text = p[4]['text']
    summary = p[2]
    p[0] = p[4]
    p[0]['text'] = '{} Filter duplicates from the output of the previous sort operation. {}'.format(sub_text, summary)

def p_group_stmt(p):
    '''
    group_stmt : GROUP summary SUBOPS sort_stmt
    '''
    sub_text = p[4]['text']
    summary = p[2]
    p[0] = p[4]
    p[0]['text'] = '{} Group the output of the previous sort operation according to the sort key. {}'.format(sub_text, summary)

def p_hashsetop_intersect_stmt(p):
    '''
    hashsetop_intersect_stmt : HASH_SET_OP INTERSECT summary SUBOPS statement
                    | HASH_SET_OP INTERSECT ALL summary SUBOPS statement
    '''
    if (p[3] == 'All'):
        summary = p[4]
        sub_text = p[6]['text']
        p[0] = p[6]
        p[0]['text'] = '{} Perform intersection with duplicates using hash set operation on output of the previous operation. {}'.format(sub_text, summary)
    else:
        summary = p[3]
        sub_text = p[5]['text']
        p[0] = p[5]
        p[0]['text'] = '{} Perform intersection without duplicates using hash set operation on output of the previous operation. {}'.format(sub_text, summary)

def p_result_stmt(p):
    '''
    result_stmt : RESULT summary SUBOPS statement
    '''
    summary = p[2]
    sub_text = p[4]['text']
    p[0] = p[4]
    p[0]['text'] = '{} Port the result of the previous operation.  {}'.format(sub_text, summary)

def p_aggregate_stmt(p):
    '''
    aggregate_stmt : HASH_AGG summary SUBOPS statement
            | AGGREGATE summary SUBOPS statement
    '''
    aggregate_summary = p[2]
    sub_text = p[4]['text']
    method = ''
    if (p[1] == 'HashAggregate'):
        method = 'without duplicates'
    else:
        method = 'with duplicates'
    p[0] = p[4]
    p[0]['text'] = '{} Perform aggregation {} on result of the previous operation to produce the output. {}'.format(sub_text, method, aggregate_summary)

def p_append_stmt(p):
    'append_stmt : APPEND summary append_args_stmt'
    sub_text = p[3]['text']
    counter = p[3]['counter']
    append_summary = p[2]
    p[0] = {}
    p[0]['text'] = '{} Append the output of the previous {} operations. {}'.format(sub_text, counter, append_summary)

def p_append_args_stmt(p):
    '''
    append_args_stmt : SUBOPS scan_stmt append_args_stmt
                | empty
    '''
    if (len(p) == 2):
        p[0] = {}
        p[0]['text'] = ''
        p[0]['counter'] = 0
    else:
        sub_text = p[2]['text']
        more_text = p[3]['text']
        p[0] = p[3]
        p[0]['text'] = '{} {}'.format(sub_text, more_text)
        p[0]['counter'] += 1

def p_scan_stmt(p):
    '''
    scan_stmt : seq_scan_stmt
                | index_scan_stmt
                | index_only_scan_stmt
                | bmp_scan_stmt
                | subquery_scan_stmt
                | result_stmt
    '''
    p[0] = p[1]

def p_join_stmt(p):
    '''
    join_stmt : nested_join_stmt
                | hash_join_stmt
                | merge_join_stmt
    '''
    p[0] = p[1]

def p_subquery_scan_stmt(p):
    '''
    subquery_scan_stmt : subquery_scan SUBOPS scan_stmt
    '''
    subquery_scan = p[1]
    alias = subquery_scan['alias']
    summary = subquery_scan['summary']
    sub_text = p[3]['text']
    p[0] = p[3]
    p[0]['text'] = '{} Set the alias of the previous scan operation as {}.  Prepare the output of {} as input for use in later operation. {}'.format(sub_text, alias, alias, summary)

def p_seq_scan_stmt(p):
    '''
    seq_scan_stmt : seq_scan
                | seq_scan condition
    '''
    seq_scan = p[1]
    table_name = seq_scan['table_name']
    text = '''Performing sequential scan by scanning through every rows on table "{}"'''.format(table_name)
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
    text = 'Performing index scan on table "{}" using B-Tree index "{}"'.format(table_name, index)
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
    text = 'Since the query result can be obtained directly on index, there is no need to access relation. Performing index scan on table "{}" getting data only from index "{}"'.format(table_name, index)
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
    '''
    bmp_scan_stmt_tail : bmp_index_scan_stmt
                | bmp_and_stmt
    '''
    p[0] = p[1]

def p_bmp_heap_scan_stmt(p):
    '''
    bmp_heap_scan_stmt : bmp_heap_scan 
                    | bmp_heap_scan condition
    '''
    heap_scan = p[1]
    table_name = heap_scan['table_name']
    text = '''After the Bitmap Index Scan which generated the bit map of pages sorted by the physical location of the row, we then accessing the rows in the order of their physical location. Performing bitmap heap scan on table "{}". '''.format(table_name)
    if (len(p) == 3):
        condition = p[2]
        text += ' with condition {}'.format(condition)
    summary = heap_scan['summary']
    text += '. {}'.format(summary)
    p[0] = {}
    p[0]['text'] = text
    p[0]['table_name'] = table_name

def p_bmp_and_stmt(p):
    '''
    bmp_and_stmt : BMP_AND summary bmp_and_stmt_tail
    '''
    sub_text = p[3]['text']
    counter = p[3]['counter']
    bmp_and_summary = p[2]
    p[0] = {}
    p[0]['text'] = '{} Perform bitmap AND on the output of the previous {} operations. {}'.format(sub_text, counter, bmp_and_summary)

def p_bmp_and_stmt_tail(p):
    '''
    bmp_and_stmt_tail : SUBOPS bmp_index_scan_stmt bmp_and_stmt_tail
                    | empty
    '''
    if (len(p) == 2):
        p[0] = {}
        p[0]['text'] = ''
        p[0]['counter'] = 0
    else:
        sub_text = p[2]['text']
        more_text = p[3]['text']
        p[0] = p[3]
        p[0]['text'] = '{} {}'.format(sub_text, more_text)
        p[0]['counter'] += 1

def p_bmp_index_scan_stmt(p):
    '''
    bmp_index_scan_stmt : bmp_index_scan 
                    | bmp_index_scan condition
    '''
    index_scan = p[1]
    table_name = index_scan['table_name']
    text = '''The interested rows are first stored in a bitmap. After the index scan is completed, the bitmap is sorted by the physical location of a row. This creates a bitmap of the pages of the relation to track pages. Performing bitmap index scan on table "{}"'''.format(table_name)
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
    text = 'First, scan the outer table "{}". {} Then, for each row of the outer table "{}", scan the inner table "{}". {} Perfoming nested loop join on table "{}" and table "{}". {}'.format(outer_table_name, outer_table_text, outer_table_name, inner_table_name, inner_table_text, outer_table_name, inner_table_name, join_summary)
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
    text = 'First, scan the first table "{}" and loaded to the hash table, using the join attribute as the hash key. {} Then, scan the second table "{}" and the appropriate values of every row found are used as hash keys to locate the matching rows in the table. {} Perfoming hash join on table "{}" and table "{}" with condition "{}". {}'.format(outer_table_name, outer_table_text, inner_table_name, inner_table_text, outer_table_name, inner_table_name, condition, join_summary)
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
    text = 'First, sort the outer table "{}". {} Then, sort the inner table "{}". Then the two relations are scanned in parallel, and matching rows are combined to form join rows. {} Perfoming merge join on table "{}" and table "{}" with condition "{}". {}'.format(outer_table_name, outer_table_text, inner_table_name, inner_table_text, outer_table_name, inner_table_name, condition, join_summary)
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

def p_subquery_scan(p):
    'subquery_scan : SUBQUERY SCAN ON ALIAS summary'
    alias = p[4]
    summary = p[5]
    p[0] = {}
    p[0]['alias'] = alias
    p[0]['summary'] = summary

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
            | onetime_filter
    '''
    p[0] = p[1]

def p_onetime_filter(p):
    'onetime_filter : ONE_TIME FILTER COLON predicate'
    p[0] = p[4]

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
    p[0] = '''This operation took {} miliseconds to initialize, {} miliseconds to complete, returning {} rows and estimated average width of row is {} bytes.'''.format(startup_cost, final_cost, rows, width)

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
        | MATCH
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
    elif (p[1] == '~~'):
        p[0] = 'match pattern'
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
    'sort_key : SORT KEY COLON attribute_list'
    p[0] = p[4]

def p_attribute_list(p):
    '''
    attribute_list : attribute_list COMMA ID
                    | ID
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = p[1] + ', ' + p[3]

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
