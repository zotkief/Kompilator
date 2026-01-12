from dataclasses import dataclass, field
from typing import List, Any
import ply.yacc as yacc
from kompilator.lexer import tokens 
from ast import *
from kompilator.codegen.conditions import *
from kompilator.codegen.expressions import *
from kompilator.codegen.helpers import *
from kompilator.codegen.statements import *
import kompilator.symbols as sym



precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'MOD')
)
    
# --- Reguły dotyczące struktury programu (1, 3-5, 7-8) ---


def p_program_all(p):
    'program_all : procedures main'

    #print("programm all")

    p[0]=programm_all(instruction_list=[])


    instruction_list: List[str] = []
    instruction_list.append("MAIN JUMP")

    appendProgramFromFile(instruction_list,"fun")

    buildProcedures(p[1].procedure_list,instruction_list)

    #for key, val in functionHashMap.items():
        #print(str(key)+" "+str(val))

    instruction_list[0]="JUMP "+str(len(instruction_list))

    decs=p[2].decs
    comms=p[2].comms
    for key,val in decs.identifierHashMap.items():
        #print(key)
        globalName="PROGRAM_"+key
        globalIdentifierHashMap[globalName]=val


    for key in globalIdentifierHashMap:
        print(str(key)+":"+str(globalIdentifierHashMap[key].dataStart))
    analizeProgram(comms,"PROGRAM_",instruction_list)
    instruction_list.append("HALT")
    p[0].instruction_list+=instruction_list
    #print(len(p[0].instruction_list))
    #for command in p[0].instruction_list:
    #    print(command)



def p_procedures(p):
    '''procedures : procedures PROCEDURE proc_head IS declarations IN commands END
                  | procedures PROCEDURE proc_head IS IN commands END
                  | empty'''
    if len(p)==2:
        p[0]=procedures([])
    elif len(p)==8:
        p[0]=p[1]
        p[0].procedure_list.append(procedure(p[3],declarations(),p[6]))
    else:
        p[0]=p[1]
        p[0].procedure_list.append(procedure(p[3],p[5],p[7]))


def p_main(p):
    '''main : PROGRAM IS declarations IN commands END
            | PROGRAM IS IN commands END'''
    
    if len(p) == 7:
        
        #print(f"main: Z deklaracjami, Liczba komend: {len(p[5].comms)}")
        
        p[0] = main(
            decs=p[3], 
            comms=p[5]
        )
    
    elif len(p) == 6:
        
        #print(f"main: Bez deklaracji, Liczba komend: {len(p[4].comms)}")
        
        empty_declarations = declarations()
        
        p[0] = main(
            decs=empty_declarations, 
            comms=p[4]
        )

# --- Reguły dotyczące komend (10-12) ---

def p_commands(p):
    '''commands : commands command
                | command'''
    
    #print(p[len(p)-1].commType)
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
    #print(p[1])
    if len(p) == 5 and isinstance(p[1],identifier):
        #print("command-assign",p[1],",",p[3])
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

def p_proc_head(p):
    'proc_head : pidentifier OPENB args_decl CLOSEB'
    args_declarations=p[3]
    p[0]=proc_head(p[1],args_declarations.args_tab)

    sym.functionArgumentsHashMap[p[1]] = args_declarations.args_tab

    var_name=p[1]+"_"+"return"
    dec = declaration(
        dataStart = sym.cellCounter,
        dataEnd = sym.cellCounter,
        isTable = False,
        varName = var_name,
        indexStart = 0,
        writable= True,
        readable= True,
        isRefrence= False,
        refrencedIdentifier="empty"
    )
    sym.cellCounter+=1
    globalIdentifierHashMap[var_name] = dec

    for dec_type, name in args_declarations.args_tab:
        match dec_type.t:
            case "E":
                var_name=p[1]+"_"+name
                dec = declaration(
                    dataStart = sym.cellCounter,
                    dataEnd = sym.cellCounter,
                    isTable = False,
                    varName = var_name,
                    indexStart = 0,
                    writable= True,
                    readable= True,
                    isRefrence= True,
                    refrencedIdentifier="empty"
                )
                globalIdentifierHashMap[var_name] = dec
            case "I":
                var_name=p[1]+"_"+name
                dec = declaration(
                    dataStart = sym.cellCounter,
                    dataEnd = sym.cellCounter,
                    isTable = False,
                    varName = var_name,
                    indexStart = 0,
                    writable= True,
                    readable= True,
                    isRefrence= True,
                    refrencedIdentifier="empty"
                )
                globalIdentifierHashMap[var_name] = dec
            case "O":
                var_name=p[1]+"_"+name
                dec = declaration(
                    dataStart = sym.cellCounter,
                    dataEnd = sym.cellCounter,
                    isTable = False,
                    varName = var_name,
                    indexStart = 0,
                    writable= True,
                    readable= True,
                    isRefrence= True,
                    refrencedIdentifier="empty"
                )
                globalIdentifierHashMap[var_name] = dec
            case "T":
                var_name=p[1]+"_"+name
                dec = declaration(
                    dataStart = sym.cellCounter,
                    dataEnd = sym.cellCounter,
                    isTable = True,
                    varName = var_name,
                    indexStart = 0,
                    writable= True,
                    readable= True,
                    isRefrence= True,
                    refrencedIdentifier="empty"
                )
                globalIdentifierHashMap[var_name] = dec
            
        sym.cellCounter += 1
                


def p_proc_call(p):
    'proc_call : pidentifier OPENB args CLOSEB'
    p[0]=proc_call(p[1],p[3].args_list)

# --- Deklaracje i argumenty (28-31, 33-36, 38-39) ---

def p_declarations(p):
    '''declarations : declarations COMMA pidentifier
                    | declarations COMMA pidentifier OPENTAB num COLON num CLOSETAB
                    | pidentifier
                    | pidentifier OPENTAB num COLON num CLOSETAB'''
    if len(p)==2:
        #print(p[1])
        p[0]=declarations()
        var_name=p[1]
        dec = declaration(
            dataStart = sym.cellCounter,
            dataEnd = sym.cellCounter,
            isTable = False,
            varName = var_name,
            indexStart = 0,
            writable= True,
            readable= True,
            isRefrence= False,
            refrencedIdentifier=""
        )
        sym.cellCounter += 1
        p[0].identifierHashMap[var_name] = dec
    elif len(p)==4:
        #print(p[3])
        p[0]=p[1]
        var_name=p[3]
        if var_name in p[0].identifierHashMap:
            raise ValueError(ValueError(f"Błąd: Zmienna '{var_name}' już istnieje."))
        dec = declaration(
            dataStart = sym.cellCounter,
            dataEnd = sym.cellCounter,
            isTable = False,
            varName = var_name,
            indexStart = 0,
            writable= True,
            readable= True,
            isRefrence= False,
            refrencedIdentifier=""
        )
        sym.cellCounter += 1
        p[0].identifierHashMap[var_name] = dec
    elif len(p)==7:
        #print(p[1])
        if p[5]<p[3]:
            #error
            pass
        p[0]=declarations()
        var_name=p[1]
        if p[3]>p[5]:
            raise ValueError("błąd indeksów tablic")
        sym.cellCounter=max(sym.cellCounter,p[3])
        dec = declaration(
            dataStart = sym.cellCounter,
            dataEnd = sym.cellCounter+p[5]-p[3],
            isTable = True,
            varName = var_name,
            indexStart = p[3],
            writable= True,
            readable= True,
            isRefrence= False,
            refrencedIdentifier=""
        )
        p[0].identifierHashMap[var_name] = dec
        sym.cellCounter += (p[5]-p[3]+1)
    else:
        #print(p[3])
        var_name=p[3]
        p[0]=p[1]
        if p[7]<p[5]:
            #error
            pass
        if var_name in p[0].identifierHashMap:
            raise ValueError(f"Błąd: Zmienna '{var_name}' już istnieje.")
        if p[5]>p[7]:
            raise ValueError("błąd indeksów tablic")
        sym.cellCounter=max(sym.cellCounter,p[5])
        dec = declaration(
            dataStart = sym.cellCounter,
            dataEnd = sym.cellCounter+p[7]-p[5],
            isTable = True,
            varName = var_name,
            indexStart = p[5],
            writable= True,
            readable= True,
            isRefrence= False,
            refrencedIdentifier=""
        )
        sym.cellCounter += (p[7]-p[5]+1)
        p[0].identifierHashMap[var_name] = dec
    #print("declarations")

def p_args_decl(p):
    '''args_decl : args_decl COMMA type pidentifier
                 | type pidentifier'''
    if len(p)==3:
        p[0] = args_decl([(p[1], p[2])])
    else:
        p[0]=p[1]
        p[0].args_tab.append((p[3],p[4]))

def p_type(p):
    '''type : T
            | I
            | O
            | empty'''
    if p[1]=='T' or p[1]=='I' or p[1]=='O':
        p[0]=type(p[1])
    else:
        p[0]=type('E')

def p_args(p):
    '''args : args COMMA pidentifier
            | pidentifier'''
    if len(p)==2:
        p[0]=args([p[1]])
    else:
        p[0]=p[1]
        p[0].args_list.append(p[3])

# --- Wyrażenia i Warunki (41-46, 48-53) ---

def p_expression(p):
    '''expression : value
                  | value PLUS value
                  | value MINUS value
                  | value MUL value
                  | value DIV value
                  | value MOD value'''
    #print("expression",p[1])
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
    p[0]=condition(val1=p[1],val2=p[3],operation=p[2])

# --- Elementy podstawowe (55-60) ---

def p_value(p):
    '''value : num
             | identifier'''
    p[0]=value(p[1])

def p_pidentifier(p):
    'pidentifier : LABEL'
    p[0]=p[1]
    #print("identifier",p[1])

def p_num(p):
    'num : NUMBER'
    p[0]=p[1]
    #print("number",p[1])

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

def p_opt_newlines(p):
    '''opt_newlines : opt_newlines NEWLINE
                     | NEWLINE
                     | empty'''
    pass


# --- Funkcja obsługująca błędy parsowania (opcjonalna, ale zalecana) ---

def p_error(p):
    if p:
        print(f"Błąd składni w tokenie: {p.type}, linia {p.lineno}")
    else:
        print("Błąd składni na końcu pliku (Unexpected end of file)")
    
start = 'program_all'

parser = yacc.yacc(debugfile='parser.txt', tabmodule='parsetab')
