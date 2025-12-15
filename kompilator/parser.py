from dataclasses import dataclass, field
from typing import List, Any
import ply.yacc as yacc
from kompilator.lexer import tokens 
from ast import *
from ast import *
from kompilator.codegen.conditions import *
from kompilator.codegen.expressions import *
from kompilator.codegen.helpers import *
from kompilator.codegen.statements import *



precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'MOD')
)
    
# --- Reguły dotyczące struktury programu (1, 3-5, 7-8) ---

def p_optional_terminator(p):
    '''optional_terminator : empty optional_terminator
                           | empty'''
    pass

def p_program_all(p): #TODO
    'program_all : procedures main optional_terminator'

    print("programm all")

    p[0]=programm_all(instruction_list=[])


    instruction_list: List[str] = []
    instruction_list.append("MAIN JUMP")

    appendProgramFromFile(instruction_list,"fun")

    instruction_list[0]="JUMP "+str(len(instruction_list))

    decs=p[2].decs
    comms=p[2].comms
    for key,val in decs.identifierHashMap.items():
        globalName="PROGRAM_"+key
        globalIdentifierHashMap[globalName]=val


    analizeProgram(comms,"PROGRAM_",instruction_list)
    p[0].instruction_list+=instruction_list
    print(len(p[0].instruction_list))
    for command in p[0].instruction_list:
        print(command)

def p_procedures(p): #TODO
    '''procedures : procedures PROCEDURE proc_head IS declarations IN commands END
                  | procedures PROCEDURE proc_head IS IN commands END
                  | empty'''
    pass

def p_main(p):
    '''main : PROGRAM IS declarations IN commands END
            | PROGRAM IS IN commands END'''
    
    if len(p) == 7:
        
        print(f"main: Z deklaracjami, Liczba komend: {len(p[5].comms)}")
        
        p[0] = main(
            decs=p[3], 
            comms=p[5]
        )
    
    elif len(p) == 6:
        
        print(f"main: Bez deklaracji, Liczba komend: {len(p[4].comms)}")
        
        empty_declarations = declarations()
        
        p[0] = main(
            decs=empty_declarations, 
            comms=p[4]
        )

# --- Reguły dotyczące komend (10-12) ---

def p_commands(p):
    '''commands : commands command
                | command'''
    
    print(p[len(p)-1].commType)
    if len(p) == 3:
        p[0] = p[1]
        p[0].comms.append(p[2])
    else:
        p[0] = commands(comms=[p[1]])



# --- Reguły pojedynczej komendy (13-22) ---

def p_command(p):
    '''command : identifier ASSIGN expression SEMICOLON
               | IF condition THEN commands ELSE commands ENDIF
               | IF condition THEN commands ENDIF
               | WHILE condition DO commands ENDWHILE
               | REPEAT commands UNTIL condition SEMICOLON
               | FOR pidentifier FROM value TO value DO commands ENDFOR
               | FOR pidentifier FROM value DOWNTO value DO commands ENDFOR
               | proc_call SEMICOLON
               | READ identifier SEMICOLON
               | WRITE value SEMICOLON'''
    print(p[1])
    if len(p) == 5 and isinstance(p[1],identifier):
        print("command-assign",p[1],",",p[3])
        p[0] = command(
            commType="ASSIGN",
            arguments=[p[1], p[3]]
        )
    # IF...ELSE...ENDIF (len=8)
    elif len(p) == 8:
        p[0] = command(
            commType="IFELSE",
            arguments=[p[2], p[4], p[6]]  # condition, commands_true, commands_false
        )
    # IF...ENDIF (len=6)
    elif len(p) == 6 and p[1] == "IF":
        p[0] = command(
            commType="IF",
            arguments=[p[2], p[4]]  # condition, commands_true
        )
    # WHILE...ENDWHILE (len=6)
    elif len(p) == 6 and p[1] == "WHILE":
        p[0] = command(
            commType="WHILE",
            arguments=[p[2], p[4]]  # condition, commands
        )
    # REPEAT...UNTIL (len=6)
    elif len(p) == 6 and p[1] == "REPEAT":
        # W Twojej oryginalnej regule arguments=[p[2], p[4]]
        # to jest prawdopodobnie [commands, condition].
        p[0] = command(
            commType="REPEAT",
            arguments=[p[2], p[4]]
        )
    # FOR...TO...ENDFOR (len=10, p[5]=="TO")
    elif len(p) == 10 and p[5] == "TO":
        p[0] = command(
            commType="FORTO",
            arguments=[p[2], p[4], p[6], p[8]] # pidentifier, value_start, value_end, commands
        )
    # FOR...DOWNTO...ENDFOR (len=10, p[5]=="DOWNTO")
    elif len(p) == 10 and p[5] == "DOWNTO":
        p[0] = command(
            commType="FORDOWN",
            arguments=[p[2], p[4], p[6], p[8]] # pidentifier, value_start, value_end, commands
        )
    # PROC_CALL SEMICOLON (len=3)
    elif len(p) == 3:
        p[0] = command(
            commType="PROC_CALL",
            arguments=[p[1]]  # proc_call
        )
    # READ identifier SEMICOLON (len=4)
    elif len(p) == 4 and p[1] == "READ":
        p[0] = command(
            commType="READ",
            arguments=[p[2]]  # identifier
        )
    # WRITE value SEMICOLON (len=4)
    else: # Zmieniono else na elif dla lepszej kontroli
        p[0] = command(
            commType="WRITE",
            arguments=[p[2]]  # value
        )  


# --- Nagłówki i wywołania procedur (24, 26) ---

def p_proc_head(p): #TODO
    'proc_head : pidentifier OPENB args_decl CLOSEB'
    p[0]=proc_head()
    pass

def p_proc_call(p): #TODO
    'proc_call : pidentifier OPENB args CLOSEB'
    pass

# --- Deklaracje i argumenty (28-31, 33-36, 38-39) ---

def p_declarations(p):
    '''declarations : declarations COMMA pidentifier
                    | declarations COMMA pidentifier OPENTAB num COLON num CLOSETAB
                    | pidentifier
                    | pidentifier OPENTAB num COLON num CLOSETAB'''
    global cellCounter
    if len(p)==2:
        p[0]=declarations()
        var_name=p[1]
        dec = declaration(
            dataStart = cellCounter,
            dataEnd = cellCounter,
            isTable = False,
            varName = var_name,
            indexStart = 0,
            writable= True,
            readable= True
        )
        cellCounter += 1
        p[0].identifierHashMap[var_name] = dec
    elif len(p)==4:
        p[0]=p[1]
        var_name=p[3]
        if var_name in p[0].identifierHashMap:
            raise ValueError(f"Błąd: Zmienna '{var_name}' już istnieje.")
        dec = declaration(
            dataStart = cellCounter,
            dataEnd = cellCounter,
            isTable = False,
            varName = var_name,
            indexStart = 0,
            writable= True,
            readable= True
        )
        cellCounter += 1
        p[0].identifierHashMap[var_name] = dec
    elif len(p)==7:
        if p[5]<p[3]:
            #error
            pass
        p[0]=declarations()
        var_name=p[1]
        dec = declaration(
            dataStart = cellCounter,
            dataEnd = cellCounter+p[5]-p[3],
            isTable = True,
            varName = var_name,
            indexStart = p[3],
            writable= True,
            readable= True
        )
    else:
        var_name=p[3]
        p[0]=p[1]
        if p[7]<p[5]:
            #error
            pass
        if var_name in p[0].identifierHashMap:
            raise ValueError(f"Błąd: Zmienna '{var_name}' już istnieje.")
        dec = declaration(
            dataStart = cellCounter,
            dataEnd = cellCounter+p[7]-p[5],
            isTable = True,
            varName = var_name,
            indexStart = p[5],
            writable= True,
            readable= True
        )
        cellCounter += 1
        p[0].identifierHashMap[var_name] = dec
    print("declarations")

def p_args_decl(p): #TODO
    '''args_decl : args_decl COMMA type pidentifier
                 | type pidentifier'''
    pass

def p_type(p): #TODO
    '''type : T
            | I
            | O
            | empty'''
    pass

def p_args(p): #TODO
    '''args : args COMMA pidentifier
            | pidentifier'''
    pass

# --- Wyrażenia i Warunki (41-46, 48-53) ---

def p_expression(p):
    '''expression : value
                  | value PLUS value
                  | value MINUS value
                  | value MUL value
                  | value DIV value
                  | value MOD value'''
    print("expression",p[1])
    if len(p)==2:
        p[0]=expression(
            isDouble=False,
            val1=p[1],
            val2=p[1],
            operation=""
        )
    else:
        p[0]=expression(
            isDouble=True,
            val1=p[1],
            val2=p[3],
            operation=p[2]
        )


def p_condition(p):
    '''condition : value EQUAL value
                 | value UNEQUAL value
                 | value GREATER value
                 | value LESSER value
                 | value GREATEREQUAL value
                 | value LESSEREQUAL value'''
    p[0]=condition()
    p[0].val1=p[1]
    p[0].val2=p[3]
    p[0].operation=p[2]

# --- Elementy podstawowe (55-60) ---

def p_value(p):
    '''value : num
             | identifier'''
    p[0]=p[1]
    print("value",p[1])

def p_pidentifier(p):
    'pidentifier : LABEL'
    p[0]=p[1]
    print("identifier",p[1])

def p_num(p):
    'num : NUMBER'
    p[0]=p[1]
    print("number",p[1])

def p_identifier(p):
    '''identifier : pidentifier
                  | pidentifier OPENTAB pidentifier CLOSETAB
                  | pidentifier OPENTAB num CLOSETAB'''
    p[0]=identifier()
    if len(p)==2:
        p[0].name=p[1]
        p[0].isTable=False
    else:
        p[0].name=p[1]
        p[0].isTable=True
        p[0].index=p[3]


# --- Reguła dla pustej produkcji (wymagana przez PLY dla reguł 5 i 36) ---

def p_empty(p):
    'empty :'
    pass

def p_ignoreNewline(p):
    'empty : NEWLINE'
    pass

# --- Funkcja obsługująca błędy parsowania (opcjonalna, ale zalecana) ---

def p_error(p):
    if p:
        print(f"Błąd składni w tokenie: {p.type}, linia {p.lineno}")
    else:
        print("Błąd składni na końcu pliku (Unexpected end of file)")
    
start = 'program_all'

parser = yacc.yacc(debugfile='parser.txt', tabmodule='parsetab')
