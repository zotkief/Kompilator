from ..classes import *
from .helpers import *
from ..symbols import *

def loadValue(v: value, register: str, prefix: str, instruction_list: List[str]):
    if isinstance(v.val, int):
        constructNumberInH(v.val, instruction_list)
        if register != "h":
            instruction_list.append("SWP h")
            instruction_list.append("SWP " + register)
    else:
        curr_id = v.val
        dec=globalIdentifierHashMap[prefix+curr_id.name]
        if not dec.isTable:
            name=curr_id.name
            name=prefix+name

            if name not in globalIdentifierHashMap:
                raise Exception("niezadeklarowana zmienna:"+name)
            
            if (not dec.readable):
                raise ValueError("zmienna nie jest odczytywalna: "+dec.varName)

            constructNumberInH(dec.dataStart,instruction_list)
            instruction_list.append("SWP h")
            instruction_list.append("SWP b")
            instruction_list.append("RLOAD b")
            
            if dec.isRefrence:
                instruction_list.append("SWP b")
                instruction_list.append("RLOAD b")

            instruction_list.append("SWP "+register)
        elif isinstance(curr_id.index,int):
            if (not prefix+curr_id.name in globalIdentifierHashMap):
                raise ValueError("niezadeklarowana zmienna")

            current_index=curr_id.index-dec.indexStart

            if dec.isRefrence:
                constructNumberInH(dec.dataStart,instruction_list)
                instruction_list.append("SWP h")
                instruction_list.append("SWP b")
                constructNumberInH(current_index,instruction_list)
                instruction_list.append("RLOAD b")
                instruction_list.append("ADD h")
                instruction_list.append("SWP b")
                instruction_list.append("RLOAD b")
                instruction_list.append("SWP "+register)
            else:
                if current_index<dec.dataStart or current_index>dec.dataEnd:
                    #raise "indeks poza zakresem"
                    pass
                constructNumberInH(dec.dataStart+current_index,instruction_list)
                instruction_list.append("SWP h")
                instruction_list.append("SWP b")
                instruction_list.append("RLOAD b")
                instruction_list.append("SWP "+register)
        else:
            if (not prefix+curr_id.name in globalIdentifierHashMap):
                raise ValueError("niezadeklarowana zmienna (tablica)")
            if (not prefix+curr_id.index in globalIdentifierHashMap):
                raise ValueError("niezadeklarowana zmienna (indeks)")
            indexDec=globalIdentifierHashMap[prefix+curr_id.index]
            if (indexDec.isTable):
                raise ValueError("index jest tablicą")
            if (not dec.readable):
                raise ValueError("wartość nie jest odczytywalna")
            if (not indexDec.readable):
                raise ValueError("indeks nie jest odczytywalny")
            

            if (not dec.isRefrence) and (not indexDec.isRefrence):

                instruction_list.append("LOAD "+str(indexDec.dataStart))

                instruction_list.append("SWP b")
                constructNumberInH(dec.dataStart,instruction_list)
                instruction_list.append("SWP b")
                instruction_list.append("ADD h")

                instruction_list.append("SWP b")
                constructNumberInH(dec.indexStart,instruction_list)
                instruction_list.append("SWP b")
                instruction_list.append("SUB h")

                instruction_list.append("SWP c")

                instruction_list.append("RLOAD c")

                instruction_list.append("SWP "+register)
            elif (not dec.isRefrence) and (indexDec.isRefrence):

                instruction_list.append("LOAD "+str(indexDec.dataStart))

                instruction_list.append("SWP b")
                instruction_list.append("RLOAD b")

                instruction_list.append("SWP b")
                constructNumberInH(dec.dataStart,instruction_list)
                instruction_list.append("SWP b")
                instruction_list.append("ADD h")

                instruction_list.append("SWP b")
                constructNumberInH(dec.indexStart,instruction_list)
                instruction_list.append("SWP b")
                instruction_list.append("SUB h")

                instruction_list.append("SWP c")

                instruction_list.append("RLOAD c")

                instruction_list.append("SWP "+register)
            elif (dec.isRefrence) and (not indexDec.isRefrence):

                
                instruction_list.append("LOAD "+str(indexDec.dataStart))
                instruction_list.append("SWP c")
                instruction_list.append("LOAD "+str(dec.dataStart))
                instruction_list.append("ADD c")
                instruction_list.append("SWP c")
                instruction_list.append("RLOAD c")
                instruction_list.append("SWP "+register)

            else:
                
                instruction_list.append("LOAD "+str(indexDec.dataStart))
                instruction_list.append("SWP c")
                instruction_list.append("RLOAD c")
                instruction_list.append("SWP c")

                instruction_list.append("LOAD "+str(dec.dataStart))
                instruction_list.append("ADD c")
                instruction_list.append("SWP b")
                instruction_list.append("RLOAD b")

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
        if not dec.writable:
            raise ValueError("zmienna nie nadpisywalna: "+dec.varName)

        if dec.isRefrence:
            instruction_list.append("LOAD "+str(dec.dataStart))
            instruction_list.append("SWP b")
            instruction_list.append("SWP "+register)
            instruction_list.append("RSTORE b")
        else:
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

        if not dec.writable:
            raise ValueError("zmienna nie jest nadpisywalna")

        if dec.isRefrence:
            constructNumberInH(dec.dataStart,instruction_list)
            instruction_list.append("SWP h")
            instruction_list.append("SWP b")
            constructNumberInH(current_index,instruction_list)
            instruction_list.append("RLOAD b")
            instruction_list.append("ADD h")
            instruction_list.append("SWP b")

            instruction_list.append("SWP "+register)

            instruction_list.append("RSTORE b")
        else:
            current_index=curr_id.index-dec.indexStart
            instruction_list.append("SWP "+register)
            instruction_list.append("STORE "+str(dec.dataStart+current_index))
    else:
        dec=globalIdentifierHashMap[prefix+curr_id.name]
        if (not prefix+curr_id.name in globalIdentifierHashMap):
            raise ValueError("niezadeklarowana zmienna (tablica)")
        if (not prefix+curr_id.index in globalIdentifierHashMap):
            raise ValueError("niezadeklarowana zmienna (indeks)")
        indexDec=globalIdentifierHashMap[prefix+curr_id.index]
        if (indexDec.isTable):
            raise ValueError("index jest tablicą")
        if (not dec.writable):
            raise ValueError("wartość nie jest odczytywalna")
        if (not indexDec.readable):
            raise ValueError("indeks nie jest odczytywalny: "+indexDec.varName)
        

        if (not dec.isRefrence) and (not indexDec.isRefrence):

            instruction_list.append("LOAD "+str(indexDec.dataStart))

            instruction_list.append("SWP b")
            constructNumberInH(dec.dataStart,instruction_list)
            instruction_list.append("SWP b")
            instruction_list.append("ADD h")

            instruction_list.append("SWP b")
            constructNumberInH(dec.indexStart,instruction_list)
            instruction_list.append("SWP b")
            instruction_list.append("SUB h")

            instruction_list.append("SWP c")

            instruction_list.append("SWP "+register)

            instruction_list.append("RSTORE c")
        elif (not dec.isRefrence) and (indexDec.isRefrence):

            instruction_list.append("LOAD "+str(indexDec.dataStart))

            instruction_list.append("SWP b")
            instruction_list.append("RLOAD b")

            instruction_list.append("SWP b")
            constructNumberInH(dec.dataStart,instruction_list)
            instruction_list.append("SWP b")
            instruction_list.append("ADD h")

            instruction_list.append("SWP b")
            constructNumberInH(dec.indexStart,instruction_list)
            instruction_list.append("SWP b")
            instruction_list.append("SUB h")

            instruction_list.append("SWP c")

            instruction_list.append("SWP "+register)

            instruction_list.append("RSTORE c")
        elif (dec.isRefrence) and (not indexDec.isRefrence):

            
            instruction_list.append("LOAD "+str(dec.dataStart))
            instruction_list.append("SWP c")
            instruction_list.append("LOAD "+str(indexDec.dataStart))
            instruction_list.append("ADD c")
            instruction_list.append("SWP c")
            instruction_list.append("SWP "+register)
            instruction_list.append("RSTORE c")

        else:
            
            instruction_list.append("LOAD "+str(indexDec.dataStart))
            instruction_list.append("SWP c")
            instruction_list.append("RLOAD c")
            instruction_list.append("SWP c")

            instruction_list.append("LOAD "+str(dec.dataStart))
            instruction_list.append("ADD c")
            instruction_list.append("SWP b")
            instruction_list.append("SWP "+register)
            instruction_list.append("RSTORE b")


