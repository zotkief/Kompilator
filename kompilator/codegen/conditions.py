from .expressions import *
from ..classes import *

def buildCondition(cond : condition,prefix : str, instruction_list : List[str],jumpsToChange:List[int]):
    match cond.operation:
        case "=":
            loadValue(cond.val1,"e",prefix,instruction_list)
            loadValue(cond.val2,"f",prefix,instruction_list)
            instruction_list.append("RST a")
            instruction_list.append("ADD e")
            instruction_list.append("SUB f")
            instruction_list.append("JPOS ")
            jumpsToChange.append(len(instruction_list)-1)
            instruction_list.append("RST a")
            instruction_list.append("ADD f")
            instruction_list.append("SUB e")
            instruction_list.append("JPOS ")
            jumpsToChange.append(len(instruction_list)-1)
        case "!=":
            loadValue(cond.val1, "e", prefix, instruction_list)
            loadValue(cond.val2, "f", prefix, instruction_list)

            jumpsIfTrue=[]

            # a = e - f
            instruction_list.append("RST a")
            instruction_list.append("ADD e")
            instruction_list.append("SUB f")

            instruction_list.append("JPOS ")
            jumpsIfTrue.append(len(instruction_list) - 1)

            # a = f - e
            instruction_list.append("RST a")
            instruction_list.append("ADD f")
            instruction_list.append("SUB e")

            instruction_list.append("JPOS ")
            jumpsIfTrue.append(len(instruction_list) - 1)
            instruction_list.append("JUMP ")
            jumpsToChange.append(len(instruction_list) - 1)
            for i in jumpsIfTrue:
                instruction_list[i]+=str(len(instruction_list))
            

        case ">":
            loadValue(cond.val1,"e",prefix,instruction_list)
            loadValue(cond.val2,"f",prefix,instruction_list)
            instruction_list.append("RST a")
            instruction_list.append("ADD f")
            instruction_list.append("INC a")
            instruction_list.append("SUB e")
            instruction_list.append("JPOS ")
            jumpsToChange.append(len(instruction_list)-1)
        case "<":
            loadValue(cond.val1,"e",prefix,instruction_list)
            loadValue(cond.val2,"f",prefix,instruction_list)
            instruction_list.append("RST a")
            instruction_list.append("ADD e")
            instruction_list.append("INC a")
            instruction_list.append("SUB f")
            instruction_list.append("JPOS ")
            jumpsToChange.append(len(instruction_list)-1)
        case ">=":
            loadValue(cond.val1,"e",prefix,instruction_list)
            loadValue(cond.val2,"f",prefix,instruction_list)
            instruction_list.append("RST a")
            instruction_list.append("ADD e")
            instruction_list.append("INC a")
            instruction_list.append("SUB f")
            instruction_list.append("JZERO ")
            jumpsToChange.append(len(instruction_list)-1)
        case "<=":
            loadValue(cond.val1,"e",prefix,instruction_list)
            loadValue(cond.val2,"f",prefix,instruction_list)
            instruction_list.append("RST a")
            instruction_list.append("ADD f")
            instruction_list.append("INC a")
            instruction_list.append("SUB e")
            instruction_list.append("JZERO ")
            jumpsToChange.append(len(instruction_list)-1)
        case _:
            #error
            pass
            