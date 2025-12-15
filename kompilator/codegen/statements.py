from ..classes import *
from .conditions import *

def analizeProgram(commands : commands ,prefix : str,instruction_list: List[str]):

    comms = commands.comms

    for comm in comms:
        match comm.commType:
            case "ASSIGN":
                exp = comm.arguments[1]
                p_id = comm.arguments[0]
                loadExpression(exp,"h",prefix,instruction_list)
                uploadFromRegister(p_id,"h",prefix,instruction_list)
            case "IF":
                cond:condition = comm.arguments[0]
                subcommands = comm.arguments[1]
                jumpsIfFail = []
                buildCondition(cond,prefix,instruction_list,jumpsIfFail)
                analizeProgram(subcommands,prefix,instruction_list)
                for i in jumpsIfFail:
                    instruction_list[i]+= str(len(instruction_list))
            case "IFELSE":
                cond:condition = comm.arguments[0]
                subcommandsTrue = comm.arguments[1]
                subcommandsFail = comm.arguments[2]
                jumpsIfFail = []
                buildCondition(cond,prefix,instruction_list,jumpsIfFail)
                analizeProgram(subcommandsTrue,prefix,instruction_list)
                instruction_list.append("JUMP ")
                jumpIfTrue = len(instruction_list)-1
                for i in jumpsIfFail:
                    instruction_list[i]+= str(len(instruction_list))

                analizeProgram(subcommandsFail,prefix,instruction_list)
                instruction_list[jumpIfTrue]+= str(len(instruction_list))
            case "WHILE":
                cond:condition = comm.arguments[0]
                subcommands = comm.arguments[1]
                loopBegin:int = len(instruction_list)
                jumpsIfFail = []
                buildCondition(cond,prefix,instruction_list,jumpsIfFail)
                analizeProgram(subcommands,prefix,instruction_list)
                instruction_list.append("JUMP "+str(loopBegin))
                for i in jumpsIfFail:
                    instruction_list[i]+= str(len(instruction_list))
            case "REPEAT":
                cond:condition = comm.arguments[1]
                subcommands = comm.arguments[0]
                loopBegin:int = len(instruction_list)
                jumpsIfFail = []
                analizeProgram(subcommands,prefix,instruction_list)
                buildCondition(cond,prefix,instruction_list,jumpsIfFail)
                for i in jumpsIfFail:
                    instruction_list[i]+= str(loopBegin)
            case "FORTO":
                iteratorIdentifier = identifier(False,comm.arguments[0],0)
                startValue:value = comm.arguments[1]
                endValue:value = comm.arguments[2]
                subcommands = comm.arguments[3]
                if not prefix+iteratorIdentifier in globalIdentifierHashMap:
                    raise "niezadeklarowana zmienna (iterator)"

                #assigning starting value
                exp = expression(isDouble=False,val1=startValue,val2=startValue,operation="")
                loadExpression(exp,"h",prefix,instruction_list)
                uploadFromRegister(iteratorIdentifier,"h",prefix,instruction_list)
                globalIdentifierHashMap[prefix+iteratorIdentifier].writable = False

                #generating subcommands
                loopStart=len(instruction_list)
                analizeProgram(subcommands,prefix,instruction_list)

                #creating temporary condition 
                val1 = value(iteratorIdentifier)
                cond:condition = condition(val1=val1, val2=endValue, operation="=")

                jumpsIfFail=[]
                buildCondition(cond,prefix,instruction_list,jumpsIfFail)

                #itaration
                globalIdentifierHashMap[prefix+iteratorIdentifier].writable = True
                exp = expression(
                    isDouble=False,
                    val1=value(identifier(False,iteratorIdentifier,0)),
                    val2=value(1),
                    operation="+"
                )
                loadExpression(exp,"h",prefix,instruction_list)
                uploadFromRegister(iteratorIdentifier,"h",prefix,instruction_list)


                for i in jumpsIfFail:
                    instruction_list[i]+=loopStart
            case "FORDOWN":
                iteratorIdentifier = identifier(False,comm.arguments[0],0)
                startValue:value = comm.arguments[1]
                endValue:value = comm.arguments[2]
                subcommands = comm.arguments[3]
                if not prefix+iteratorIdentifier in globalIdentifierHashMap:
                    raise "niezadeklarowana zmienna (iterator)"

                #assigning starting value
                exp = expression(isDouble=False,val1=startValue,val2=startValue,operation="")
                loadExpression(exp,"h",prefix,instruction_list)
                uploadFromRegister(iteratorIdentifier,"h",prefix,instruction_list)
                globalIdentifierHashMap[prefix+iteratorIdentifier].writable = False

                #generating subcommands
                loopStart=len(instruction_list)
                analizeProgram(subcommands,prefix,instruction_list)

                #creating temporary condition 
                val1 = value(iteratorIdentifier)
                cond:condition = condition(val1=val1, val2=endValue, operation="=")

                jumpsIfFail=[]
                buildCondition(cond,prefix,instruction_list,jumpsIfFail)

                #itaration
                globalIdentifierHashMap[prefix+iteratorIdentifier].writable = True
                exp = expression(
                    isDouble=False,
                    val1=value(identifier(False,iteratorIdentifier,0)),
                    val2=value(1),
                    operation="-"
                )
                loadExpression(exp,"h",prefix,instruction_list)
                uploadFromRegister(iteratorIdentifier,"h",prefix,instruction_list)

                for i in jumpsIfFail:
                    instruction_list[i]+=loopStart
                


