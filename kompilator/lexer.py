import ply.lex as lex

tokens = ( 'PLUS', 'MINUS', 'POW', 'MUL', 'DIV', 'MOD', 'COMM',
    'OPENB', 'CLOSEB', 'NEWLINE', 'OPENTAB', 'CLOSETAB', 'CONST', 'UNKNOWN', 'TABLE'
    'FOR', 'TO', 'DOWNTO', 'REPEAT', 'UNTIL',
    'EQUAL','ASSIGN','GREATER','LESSER', 'GREATEREQUAL', 'LESSEREQUAL', 'UNEQUAL',
    'IF', 'PROCEDURE', 'IS', 'IN', 'END', 'PROGRAM', 'THEN', 'ELSE', 'ENDIF', 'WHILE', 'DO','ENDWHILE', 'READ', 'WRITE',
    'NUMBER', 'LABEL',
    'SEMICOLON', 'COMMA', 'COLON', 'FOR', 'FROM', 'ENDFOR',
    'T','O','I'
)

reserved = {
    'FOR': 'FOR', 'TO': 'TO', 'DOWNTO': 'DOWNTO', 'REPEAT': 'REPEAT', 'UNTIL': 'UNTIL',
    'IF': 'IF', 'PROCEDURE': 'PROCEDURE', 'IS': 'IS', 'IN': 'IN', 'END': 'END',
    'THEN': 'THEN', 'ELSE': 'ELSE', 'ENDIF': 'ENDIF',
    'WHILE': 'WHILE', 'DO': 'DO', 'ENDWHILE': 'ENDWHILE',
    'READ': 'READ', 'WRITE': 'WRITE',
    'T': 'T', 'I': 'I', 'O': 'O'
}
states = (
    ('COMMENT', 'exclusive'),
)

def t_comm_START(t):
    r'\#'
    if t.lexer.lexpos - len(t.value) == 0:
        t.lexer.begin('COMMENT')
    pass

t_COMMENT_ignore = ''

def t_COMMENT_line_end(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.begin('INITIAL')
    pass
    #t.type='NEWLINE'
    #return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_LABEL(t):
    r'[a-z_]+' 
    t.type = reserved.get(t.value, 'LABEL')
    return t

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_MUL    = r'\*'
t_DIV    = r'/'
t_MOD    = r'%'

t_EQUAL         = r'='
t_ASSIGN        = r':='
t_UNEQUAL       = r'!='
t_GREATER       = r'>'
t_LESSER        = r'<'
t_GREATEREQUAL  = r'>='
t_LESSEREQUAL   = r'<'

t_OPENB     = r'\('
t_CLOSEB    = r'\)'
t_OPENTAB   = r'\['
t_CLOSETAB  = r'\]'

t_I         = r'I'
t_O         = r'O'
t_T         = r'T'

t_FOR       = r'FOR'
t_TO        = r'TO'
t_DOWNTO    = r'DOWNTO'
t_REPEAT    = r'REPEAT'
t_UNTIL     = r'UNTIL'

t_IF        = r'IF'
t_PROCEDURE = r'PROCEDURE'
t_IS        = r'IS'
t_IN        = r'IN'
t_END       = r'END'
t_PROGRAM   = r'PROGRAM'
t_THEN      = r'THEN'
t_ELSE      = r'ELSE'
t_ENDIF     = r'ENDIF'
t_WHILE     = r'WHILE'
t_DO        = r'DO'
t_ENDWHILE  = r'ENDWHILE'
t_FROM      = r'FROM'
t_ENDFOR    = r'ENDFOR'

t_READ  = r'READ'
t_WRITE = r'WRITE'

t_SEMICOLON = r'\;'
t_COMMA     = r'\,'
t_COLON     = r'\:'

"""
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.type='NEWLINE'
    return t"""

t_ignore = ' \t\n'

def t_error(t):
    print(f"Nieznany znak {t.value[0]!r} w linii {t.lexer.lineno}")
    t.lexer.skip(1)

def t_COMMENT_error(t):
    t.lexer.skip(1)

lexer = lex.lex()
