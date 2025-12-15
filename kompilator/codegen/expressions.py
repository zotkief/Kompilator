from ..classes import *
from .helpers import *
from ..symbols import *

def loadValue(val : value, register : str, prefix : str,instruction_list: List[str]):
    if isinstance(val,int):
        constructNumberInH(val,instruction_list)
        if register != "h":
            instruction_list.append("SWP h")
            instruction_list.append("SWP "+register)
    else:
        curr_id=val
        if not curr_id.isTable:
            if (not prefix+curr_id.name in globalIdentifierHashMap):
                raise "niezadeklarowana zmienna"
            dec=globalIdentifierHashMap[prefix+curr_id.name]
            if (not dec.readable):
                raise "zmienna nie jest odczytywalna"
            instruction_list.append("LOAD "+str(dec.dataStart))
            instruction_list.append("SWP "+register)
        elif isinstance(curr_id.index,int):
            if (not prefix+curr_id.name in globalIdentifierHashMap):
                raise "niezadeklarowana zmienna"
            dec=globalIdentifierHashMap[prefix+curr_id.name]

            current_index=curr_id.index-dec.indexStart

            if current_index<dec.dataStart or current_index>dec.dataEnd:
                raise "indeks poza zakresem"
            instruction_list.append("LOAD "+str(dec.dataStart+current_index))
            instruction_list.append("SWP "+register)
        else:
            if (not prefix+curr_id.name in globalIdentifierHashMap):
                raise "niezadeklarowana zmienna (tablica)"
            if (not prefix+curr_id.index in globalIdentifierHashMap):
                raise "niezadeklarowana zmienna (indeks)"
            indexDec=globalIdentifierHashMap[prefix+curr_id.index]
            if (indexDec.isTable):
                raise "zmienna nie jest tablicą"
            dec=globalIdentifierHashMap[prefix+curr_id.name]
            current_index=curr_id.index-indexDec.indexStart
            instruction_list.append("LOAD "+str(indexDec.dataStart+current_index))
            instruction_list.append("SWP g")
            instruction_list.append("RLOAD g")
            instruction_list.append("SWP "+register)

def performOperation(operation : str,instruction_list: List[str]):

    if operation=="+":
        instruction_list.append("RST a")
        instruction_list.append("ADD e")
        instruction_list.append("ADD f")
        instruction_list.append("SWP h")
    elif operation=="-":
        instruction_list.append("RST a")
        instruction_list.append("ADD e")
        instruction_list.append("SUB f")
        instruction_list.append("SWP h")
    elif operation=="*":
        instruction_list.append("CALL "+str(functionHashMap["PROGRAM_mul"]))
        instruction_list.append("RST a")
    elif operation=="/":
        instruction_list.append("CALL "+str(functionHashMap["PROGRAM_divMod"]))
        instruction_list.append("RST a")
        instruction_list.append("SWP f")
        instruction_list.append("SWP h")
    elif operation=="%":
        instruction_list.append("CALL "+str(functionHashMap["PROGRAM_divMod"]))
        instruction_list.append("RST a")
        instruction_list.append("SWP e")
        instruction_list.append("SWP h")
    else:
        pass #error



def loadExpression(exp : expression, register : str, prefix : str,instruction_list: List[str]):
    if not exp.isDouble:
        loadValue(exp.val1,"h",prefix,instruction_list)
    else: #podwójne wyrażenia
        loadValue(exp.val1,"e",prefix,instruction_list)
        loadValue(exp.val2,"f",prefix,instruction_list)
        performOperation(exp.operation,instruction_list)
    if register != "h":
        instruction_list.append("SWP h")
        instruction_list.append("SWP "+register)


def uploadFromRegister(curr_id : identifier, register : str, prefix: str,instruction_list: List[str]):
    if not curr_id.isTable:
        if (not prefix+curr_id.name in globalIdentifierHashMap):
            #error
            pass
        dec=globalIdentifierHashMap[prefix+curr_id.name]
        instruction_list.append("SWP "+register)
        instruction_list.append("STORE "+str(dec.dataStart))
    elif isinstance(curr_id.index,int):
        if (not prefix+curr_id.name in globalIdentifierHashMap):
            #error
            pass
        #if index poza zakresem 
            #error
        dec=globalIdentifierHashMap[prefix+curr_id.name]
        current_index=curr_id.index-dec.indexStart
        instruction_list.append("SWP "+register)
        instruction_list.append("STORE "+str(dec.dataStart+current_index))
    else:
        if (not prefix+curr_id.name in globalIdentifierHashMap):
            #error
            pass
        if (not prefix+curr_id.index in globalIdentifierHashMap):
            #error
            pass
        #if index poza zakresem 
            #error
        indexDec=globalIdentifierHashMap[prefix+curr_id.index]
        if (indexDec.isTable):
            #error
            pass
        dec=globalIdentifierHashMap[prefix+curr_id.name]
        current_index=curr_id.index-indexDec.indexStart
        instruction_list.append("LOAD "+str(indexDec.dataStart+current_index))
        instruction_list.append("SWP g")
        instruction_list.append("SWP "+register)
        instruction_list.append("RSTORE g")

