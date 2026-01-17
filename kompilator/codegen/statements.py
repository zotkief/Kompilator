from ..classes import *
from .conditions import *
import kompilator.symbols as sym

def analizeProgram(commands : commands ,prefix : str,instruction_list: List[str]):
    comms = commands.comms

    for comm in comms:
        match comm.commType:
            case "ASSIGN":
                exp = comm.arguments[1]
                p_id = comm.arguments[0]
                loadExpression(exp,"g",prefix,instruction_list)
                uploadFromRegister(p_id,"g",prefix,instruction_list)
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
                iterator = identifier(False, comm.arguments[0], 0)
                startValue = comm.arguments[1]
                endValue = comm.arguments[2]
                subcommands = comm.arguments[3]

                localVar=False
                key = prefix + iterator.name
                if key not in globalIdentifierHashMap:
                    localVar=True
                    globalIdentifierHashMap[key]=declaration(
                        dataStart = sym.cellCounter,
                        dataEnd = sym.cellCounter,
                        isTable = False,
                        varName = key,
                        indexStart = 0,
                        writable= True,
                        readable= True,
                        isRefrence= False,
                        refrencedIdentifier=""
                    )
                    sym.cellCounter+=1

                # ===== zmienna końcowa (z prefiksem!) =====
                forName = "FOR_" + str(sym.forCounter)
                sym.forCounter += 1
                cell = sym.cellCounter
                sym.cellCounter += 1

                globalIdentifierHashMap[prefix + forName] = declaration(
                    cell, cell, False, forName, 0, True, True,False,""
                )
                globalIdentifierHashMap[key].writable = True

                expEnd = expression(False, endValue, endValue, "")
                loadExpression(expEnd, "h", prefix, instruction_list)
                uploadFromRegister(identifier(False, forName, 0), "h", prefix, instruction_list)

                # ===== i := start =====
                expStart = expression(False, startValue, startValue, "")
                loadExpression(expStart, "h", prefix, instruction_list)
                uploadFromRegister(iterator, "h", prefix, instruction_list)

                globalIdentifierHashMap[key].writable = False

                loopStart = len(instruction_list)

                # ===== CIAŁO =====
                analizeProgram(subcommands, prefix, instruction_list)

                # ===== WARUNEK WYJŚCIA =====
                exitCond = condition(
                    value(iterator),
                    value(identifier(False, forName, 0)),
                    "="
                )
                startJumps = []
                buildCondition(exitCond, prefix, instruction_list, startJumps)
                loopEnd=len(instruction_list)
                instruction_list.append("JUMP ")

                for i in startJumps:
                    instruction_list[i] += str(len(instruction_list))


                # ===== i := i + 1 =====
                globalIdentifierHashMap[key].writable = True
                expInc = expression(True, value(iterator), value(1), "+")
                loadExpression(expInc, "h", prefix, instruction_list)
                uploadFromRegister(iterator, "h", prefix, instruction_list)
                #globalIdentifierHashMap[key].writable = False

                instruction_list.append(f"JUMP {loopStart}")

                instruction_list[loopEnd] += str(len(instruction_list))

                if localVar:
                    instruction_list.append("RST a")
                    instruction_list.append("LOAD "+str(globalIdentifierHashMap[key].dataStart))


            case "FORDOWN":

                iterator = identifier(False, comm.arguments[0], 0)
                startValue = comm.arguments[1]
                endValue = comm.arguments[2]
                subcommands = comm.arguments[3]

                key = prefix + iterator.name

                localVar=False
                if key not in globalIdentifierHashMap:
                    localVar=True
                    globalIdentifierHashMap[key]=globalIdentifierHashMap[key]=declaration(
                        dataStart = sym.cellCounter,
                        dataEnd = sym.cellCounter,
                        isTable = False,
                        varName = key,
                        indexStart = 0,
                        writable= True,
                        readable= True,
                        isRefrence= False,
                        refrencedIdentifier=""
                    )
                    sym.cellCounter+=1

                # ===== zmienna końcowa (z prefiksem!) =====
                forName = "FOR_" + str(sym.forCounter)
                sym.forCounter += 1
                cell = sym.cellCounter
                sym.cellCounter += 1

                globalIdentifierHashMap[prefix + forName] = declaration(
                    cell, cell, False, forName, 0, True, True, False, ""
                )

                expEnd = expression(False, endValue, endValue, "")
                loadExpression(expEnd, "h", prefix, instruction_list)
                uploadFromRegister(identifier(False, forName, 0), "h", prefix, instruction_list)

                # ===== i := start =====
                expStart = expression(False, startValue, startValue, "")
                loadExpression(expStart, "h", prefix, instruction_list)
                uploadFromRegister(iterator, "h", prefix, instruction_list)

                globalIdentifierHashMap[key].writable = False

                loopStart = len(instruction_list)

                # ===== CIAŁO =====
                analizeProgram(subcommands, prefix, instruction_list)

                # ===== WARUNEK WYJŚCIA =====
                exitCond = condition(
                    value(iterator),
                    value(identifier(False, forName, 0)),
                    "="
                )
                startJumps = []
                buildCondition(exitCond, prefix, instruction_list, startJumps)
                loopEnd=len(instruction_list)
                instruction_list.append("JUMP ")

                for i in startJumps:
                    instruction_list[i] += str(len(instruction_list))


                # ===== i := i + 1 =====
                globalIdentifierHashMap[key].writable = True
                expInc = expression(True, value(iterator), value(1), "-")
                loadExpression(expInc, "h", prefix, instruction_list)
                uploadFromRegister(iterator, "h", prefix, instruction_list)
                globalIdentifierHashMap[key].writable = False

                instruction_list.append(f"JUMP {loopStart}")

                instruction_list[loopEnd] += str(len(instruction_list))


                if localVar:
                    instruction_list.append("RST a")
                    instruction_list.append("LOAD "+str(globalIdentifierHashMap[key].dataStart))

            case "READ":
                instruction_list.append("READ")
                uploadFromRegister(comm.arguments[0],"a",prefix,instruction_list)
            case "WRITE":
                loadValue(comm.arguments[0],"a",prefix,instruction_list)
                instruction_list.append("WRITE")

            case "PROC_CALL":
                call=comm.arguments[0]
                proc_name=call.proc_name
                arg_call_list=call.args_list
                arg_proc_list=functionArgumentsHashMap[proc_name]

                if not len(arg_call_list)==len(arg_proc_list):
                    raise ValueError("inna liczba argumentów")
                
                for i in range(len(arg_proc_list)):
                    arg_type,arg_name=arg_proc_list[i]
                    original_dec=sym.globalIdentifierHashMap[prefix+arg_call_list[i]]
                    reference_dec=sym.globalIdentifierHashMap[proc_name+"_"+arg_name]

                    if original_dec.isRefrence:
                        instruction_list.append("LOAD "+str(original_dec.dataStart))
                        instruction_list.append("STORE "+str(reference_dec.dataStart))

                        instruction_list.append("LOAD "+str(original_dec.dataStart+1))
                        instruction_list.append("STORE "+str(reference_dec.dataStart+1))
                    elif original_dec.isTable:
                        constructNumberInH(original_dec.dataStart,instruction_list)
                        instruction_list.append("SWP h")
                        instruction_list.append("STORE "+str(reference_dec.dataStart))

                        constructNumberInH(original_dec.indexStart,instruction_list)
                        instruction_list.append("SWP h")
                        instruction_list.append("STORE "+str(reference_dec.dataStart+1))
                    else:
                        constructNumberInH(original_dec.dataStart,instruction_list)
                        instruction_list.append("SWP h")
                        instruction_list.append("STORE "+str(reference_dec.dataStart))

                        instruction_list.append("RST a")
                        instruction_list.append("STORE "+str(reference_dec.dataStart+1))

                instruction_list.append("CALL "+str(functionHashMap[proc_name]))
                        
                

def buildProcedures(procs : procedures, instruction_list: List[str]):
    for proc in procs:
        decs=proc.declarations

        for key,val in decs.identifierHashMap.items():
            globalName=proc.head.proc_name+"_"+key
            globalIdentifierHashMap[globalName]=val

        sym.functionHashMap[proc.head.proc_name] = len(instruction_list)

        instruction_list.append("STORE "+str(globalIdentifierHashMap[proc.head.proc_name+"_return"].dataStart))

        print(sym.globalIdentifierHashMap.keys())

        analizeProgram(proc.body,proc.head.proc_name+"_",instruction_list)

        instruction_list.append("LOAD "+str(globalIdentifierHashMap[proc.head.proc_name+"_return"].dataStart))
        instruction_list.append("RTRN")



