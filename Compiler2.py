import sys
import os
import re
import cPostFix
import parsing

NUM_DECLARATION = "^num\s\w+;$"
NUM_INITIALIZATION = "^num\s\w+\s=\s.*;$"
EQUALS = "^.*=.*;$"
SETNUM_EQUALTO = "^num\s\w+.*"
SETVAR_EQUALTO = "^\w+"
WRITE_STRING = "^write\s\".*\";$"
WRITE_VAR = "^write\s\w+;$"
READ_VAR = "^read\s\w+;$"
FOR_LOOP = "^for.*"
#List to keep track of errors.
ERRORS = []
#Dictionaries to keep track of variables
I_VARS = {}  #Name of var is index, contents = type, value
U_VARS = {}  #Name of var is index, contents = type, value
VARS = {} #Name of var is index, contents = i/u,type,value
VARS_V = {}#Name of var is index, content is just whatever its holding
BLOCK_STACK = [] #Keeps track of the closing statement for each block
ifstack = []
elseList = []
ELSE_STACK = []
otherLoopsCount = 0
ifcount = 0
elsecount = 0
bracketsIn = 0
caseCount = 0
switchVar = ""
switchCount = 0
procedureCount = 0
maxProcedureCount = 0
procedure = False
procedureVar = ""
procedureNames = {}
procedureInstructions = [2]  #Number of procedures... this is a very hacky way of doing this, but it works. 
p = 0

IMPORTS = {"_ExitProcess@4" : "extern"}
INSTRUCTIONS = []
DATA = []

Line_Count = 0
Exp_Count = 0
strVarCount = 0
forLoopCount = 0

def run(fileIn, fileOut):
    global ifcount
    global otherLoopsCount
    global caseCount
    global switchVar
    global switchCount
    global procedureCount
    global maxProcedureCount
    global procedure
    global procedureVar
    global procedureInstructions
    global p
    
    """[Opens the fileIn path, reads every line, gets rid of comments, adds every line that is not equal to empty to the
    INSTRUCTIONS list, then reads through the INSTRUCTIOn list and converts every instruction to assembly code]

    Args:
        fileIn (string): [Keeps a string representation of the file in path]
        fileOut (string): [Keeps a string representation of the file out path]
    """

    #print(strVarCount)
    #Open file and get rid of all comments.
    #Add them to the INSTRUCTIONS List after.
    with open(fileIn) as fi:
        mc = 0
        for line in fi:
            lineN = ""
            indOcu = 0
            if("//" in line):
                indOcu = line.find("//")
                lineN = line[:indOcu].strip()
            elif("/*" in line):
                indOcu = line.find("/*")
                lineN = line[:indOcu].strip()
                mc += 1
            elif("*/" in line and mc > 0):
                indOcu = line.find("*/")
                lineN = line[:indOcu].strip()
                mc -= 1
            elif( not mc > 0):
                lineN = line.strip()

            if(not lineN == ""):
                INSTRUCTIONS.append(lineN.lower())

    #For loop for adding correct spaces on all instructions.
    for i in range(len(INSTRUCTIONS)):
        INSTRUCTIONS[i] = parsing.fixSpacing(INSTRUCTIONS[i])

    #Moving Solo Brackets one instruction up.
    for i,v in enumerate(INSTRUCTIONS):
        if(v[0:3].lower() == "for"):
            if(not v[-1] == "{"):
                INSTRUCTIONS[i] = INSTRUCTIONS[i] + " {"
        if(v[0:1].lower() == "{"):
            INSTRUCTIONS.pop(i)

    #for i in INSTRUCTIONS:
     #   print(i)

    #creating variables
    for v, i in enumerate(INSTRUCTIONS):
        #print(i)
        if(re.search(NUM_DECLARATION, i)):
            createVariable(i)
        elif(re.search(EQUALS, i) and not i[0:2] == "if" and not i[0:5] == "write"):
            equalsFunction(i)
        elif(re.search(WRITE_STRING, i)):
            createSTRVar(i)
            if(not "_printf" in IMPORTS):
                IMPORTS["_printf"] = "extern"
            if(not "stringPrinter" in VARS):
               VARS["stringPrinter"] = "i,printer/,db \"%s\",0"
        elif(re.search(WRITE_VAR, i)):
            variable = i.split(" ")[1][:-1]
            if(variable in VARS):
                varType = VARS[variable].split(",")[1]
                ##print(varType)
                if(varType == "num" and not "numberPrinter" in VARS):
                        VARS["numberPrinter"] = "i,printer/,db \"%d\",0x0d,0x0a,0"
            if(not "_printf" in IMPORTS):
                IMPORTS["_printf"] = "extern"
        elif(re.search(READ_VAR, i)):
            variable = i.split(" ")[1][:-1]
            VARS[variable] = "u,readnum"
            if(not "_scanf" in IMPORTS):
                IMPORTS["_scanf"] = "extern"
            #ONLY FOR INTEGERS, NEED TO CHANGE IN FUTURE
            if(not "int_format" in VARS):
                VARS["int_format"] = "i,scanner/,db \"%i\", 0"
        elif(i[0:2] == "if"):
            ifstack.append("if{}".format(ifcount))
            ifcount += 1
        #Here I'll have to add more loop names when we add new ones such as while, etc.
        elif(i[0:3] == "for" or i[0:4] == "case" or i[0:6] == "switch" or i[0:7] == "default" or i[0:9] == "procedure"):
            otherLoopsCount += 1
            if(i[0:9] == "procedure"):

                procedureCount += 1
                name = i.split(" ")[1]
                varName = ""
                if(not name in procedureNames):
                    if("*" in i):
                        procedureNames[name] = "pointer"
                        varName = i.split(" ")[3] + i.split(" ")[4]
                        varName = varName[1:][:-1]
                    else:
                        procedureNames[name] = "value"
                        varName = i.split(" ")[3][:-1]
                        
                
                #print(varName)
                if(not varName in VARS):
                    varType = i.split(" ")[2][1:]
                    VARS[varName] = "u,{}".format(varType)
                    

        elif(i == "}"):
            if(otherLoopsCount > 0):
                otherLoopsCount -= 1
            elif INSTRUCTIONS[v+1] == "else":
                print("foundelse")
                elseList.append(ifstack.pop())
                ifstack.append("else")
            else:
                ifstack.pop()

    ifcount = 0
    
############PRINTING OUT TO FILE OUT#############
    with open(fileOut, 'w') as fo:
        #Writing export header.
        fo.write(";-----------------------------\n"+
                 "; exports\n"+
                 ";-----------------------------\n"+
                "global _main\n"+
                "EXPORT _main\n\n")

        #Writing out header for imports
        fo.write(";-----------------------------\n"+
                "; imports\n"+
                ";-----------------------------\n")
        for i in IMPORTS:
            fo.write("{} {}\n".format(IMPORTS[i], i))

        fo.write("\n")

        #Header for Vars
        fo.write(";-----------------------------\n"+
                "; Initialiazed vars\n"+
                ";-----------------------------\n"+
                "section .data USE32\n")

        #Writing out Initialized variables
        for i in VARS:
            data = VARS[i].split(",")
            if(data[0] == "i"):  #Checking if its initialized or uninitialized
                if(data[1] == "num"): #Checking the type of the variable
                    fo.write("{} dd {}\n".format(i, data[2]))
                elif("printer" in data[1]): #Checking if its a printer.
                    data = VARS[i].split("/,")
                    fo.write("{} {}\n".format(i,data[1]))
                elif("scanner" in data[1]):
                    data = VARS[i].split("/,")
                    fo.write("{} {}\n".format(i,data[1]))
                elif(data[1] == "str"):
                    fo.write("{} db {},0x0d,0x0a,0\n".format(data[2], i))

        fo.write("\n")

        fo.write(";-----------------------------\n"+
        "; Unitialiazed vars\n"+
        ";-----------------------------\n"+
        "section .bss USE32\n"+
        "temp resd 1\n"+
        "temp2 resd 1\n"+
        "temp3 resd 1\n"+
        "temp4 resd 1\n")

        #Writing out Unitialized variables
        for i in VARS:
            data = VARS[i].split(",")
            if(data[0] == "u"):  #Checking if its initialized or uninitialized
                if(data[1] == "num"): #Checking the type of the variable
                    fo.write("{} resd 1\n".format(i))
                elif(data[1] == "readnum"):
                    fo.write("{} resd 1\n".format(i))

        fo.write("\n")

        fo.write(";-----------------------------\n"+
        "; Code! (execution starts at _main)\n"+ 
        ";-----------------------------\n"+
        "section .code USE32\n")

        fo.write("_main:\n\n")

        maxProcedureCount = procedureCount

        for i in INSTRUCTIONS:
            #This first if will check if the instruction is a set instruction for example var1 = var2 or var1 = var2 + 4, '=' being the important factor
            if(re.search(EQUALS, i) and not i[0:2] == "if" and not i[0:5] == "write"):
                
                leftSide = i.split("=")[0].strip()
                rightSide = i.split("=")[1].strip()[:-1]
                if(re.search(NUM_INITIALIZATION, i)):    #This will happen if theres a num \s var = something.
                    varName = i.split("=")[0].split(" ")[1]
                    if('-' in rightSide or '+' in rightSide or '^' in rightSide or '*' in rightSide):
                        print("Not yet implement: {}".format(i))
                        print("AE")
                    else:
                        if(not isInt(rightSide)):
                            tmp = VARS[rightSide].split(",")
                            varType = tmp[1]
                            varValue = tmp[2]
                            VARS[varName] = "i,{},{}".format(varType, varValue)

                            fo.write("mov edi, DWORD[{}]\n".format(rightSide)+
                                     "mov DWORD[{}], edi\n\n".format(varName))


                        elif(isInt(rightSide)):
                            tmp = VARS[varName].split(",")
                            VARS[varName] = "i,{},{}".format(tmp[1],rightSide)

                            fo.write("mov edi, {}\n".format(rightSide)+
                                     "mov DWORD[{}], edi\n\n".format(varName))
                elif(re.search(SETVAR_EQUALTO, leftSide)):
                    global Exp_Count
                    global forLoopCount
                    global bracketsIn
                    global elseCount
                    varName = i.split("=")[0].strip()
                    #print(varName)
                    if('-' in rightSide or '+' in rightSide or '^' in rightSide or '*' in rightSide):
                        postFix = cPostFix.infixToPostfix(rightSide)
                        #print(postFix)
                        operators = ['-', '+', '*', '/', '^']
                        temp1 = False
                        temp2 = False
                        temp3 = False
                        temp4 = False

                        while(not len(postFix) == 0):
                            for index, v in enumerate(postFix):
                                if(v in operators):
                                    fOI = index - 2
                                    sOI = index - 1

                                    if(not temp1 and not temp2 and not temp3):
                                        temp1 = True
                                        temp = "temp"
                                    elif(temp1):
                                        temp = "temp"
                                    elif(temp2):
                                        temp = "temp2"
                                    elif(temp3):
                                        temp = "temp3"
                                    elif(temp4):
                                        temp = "temp4"

                                    if(v == '*'):
                                        if(isInt(postFix[fOI])):
                                            if(isInt(postFix[sOI])):
                                                fo.write("mov edi, {}\n".format(postFix[fOI])+
                                                    "imul edi, {}\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                            else:
                                                fo.write("mov edi, {}\n".format(postFix[fOI])+
                                                    "imul edi, DWORD[{}]\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            if(isInt(postFix[sOI])):
                                                fo.write("mov edi, DWORD[{}]\n".format(postFix[fOI])+
                                                    "imul edi, {}\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                            else:
                                                fo.write("mov edi, DWORD[{}]\n".format(postFix[fOI])+
                                                    "imul edi, DWORD[{}]\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                    elif(v == '+'):
                                        if(isInt(postFix[fOI])):
                                            if(isInt(postFix[sOI])):
                                                fo.write("mov edi, {}\n".format(postFix[fOI])+
                                                    "add edi, {}\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                            else:
                                                fo.write("mov edi, {}\n".format(postFix[fOI])+
                                                    "add edi, DWORD[{}]\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            if(isInt(postFix[sOI])):
                                                fo.write("mov edi, DWORD[{}]\n".format(postFix[fOI])+
                                                    "add edi, {}\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                            else:
                                                fo.write("mov edi, DWORD[{}]\n".format(postFix[fOI])+
                                                    "add edi, DWORD[{}]\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                    elif(v == '-'):
                                        if(isInt(postFix[fOI])):
                                            if(isInt(postFix[sOI])):
                                                fo.write("mov edi, {}\n".format(postFix[fOI])+
                                                    "sub edi, {}\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                            else:
                                                fo.write("mov edi, {}\n".format(postFix[fOI])+
                                                    "sub edi, DWORD[{}]\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            if(isInt(postFix[sOI])):
                                                fo.write("mov edi, DWORD[{}]\n".format(postFix[fOI])+
                                                    "sub edi, {}\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                            else:
                                                fo.write("mov edi, DWORD[{}]\n".format(postFix[fOI])+
                                                    "sub edi, DWORD[{}]\n".format(postFix[sOI])+
                                                    "mov DWORD[{}], edi\n\n".format(temp))
                                    elif(v == '^'):
                                        if(isInt(postFix[fOI])):
                                            if(isInt(postFix[sOI])):
                                                fo.write("xor edi, edi\n"+
                                                        "mov eax, 0x00000001\n"+
                                                        "_exp_top_{}:\n".format(Exp_Count)+
                                                        "cmp edi, {}\n".format(postFix[sOI])+
                                                        "jz _exp_out_{}\n".format(Exp_Count)+
                                                        "imul eax, {}\n".format(postFix[fOI])+
                                                        "inc edi\n"+
                                                        "jmp _exp_top_{}\n".format(Exp_Count)+
                                                        "_exp_out_{}:\n".format(Exp_Count)+
                                                        "mov DWORD[{}], eax\n\n".format(temp))
                                            else:
                                                fo.write("xor edi, edi\n"+
                                                        "mov eax, 0x00000001\n"+
                                                        "_exp_top_{}:\n".format(Exp_Count)+
                                                        "cmp edi, DWORD[{}]\n".format(postFix[sOI])+
                                                        "jz _exp_out_{}\n".format(Exp_Count)+
                                                        "imul eax, {}\n".format(postFix[fOI])+
                                                        "inc edi\n"+
                                                        "jmp _exp_top_{}\n".format(Exp_Count)+
                                                        "_exp_out_{}:\n".format(Exp_Count)+
                                                        "mov DWORD[{}], eax\n\n".format(temp))
                                        else:
                                            if(isInt(postFix[sOI])):
                                                fp.write("xor edi, edi\n"+
                                                        "mov eax, 0x00000001\n"+
                                                        "_exp_top_{}:\n".format(Exp_Count)+
                                                        "cmp edi, {}\n".format(postFix[sOI])+
                                                        "jz _exp_out_{}\n".format(Exp_Count)+
                                                        "imul eax, DWORD[{}]\n".format(postFix[fOI])+
                                                        "inc edi\n"+
                                                        "jmp _exp_top_{}\n".format(Exp_Count)+
                                                        "_exp_out_{}:\n".format(Exp_Count)+
                                                        "mov DWORD[{}], eax\n\n".format(temp))
                                            else:
                                                fp.write("xor edi, edi\n"+
                                                        "mov eax, 0x00000001\n"+
                                                        "_exp_top_{}:\n".format(Exp_Count)+
                                                        "cmp edi, DWORD[{}]\n".format(postFix[sOI])+
                                                        "jz _exp_out_{}\n".format(Exp_Count)+
                                                        "imul eax, DWORD[{}]\n".format(postFix[fOI])+
                                                        "inc edi\n"+
                                                        "jmp _exp_top_{}\n".format(Exp_Count)+
                                                        "_exp_out_{}:\n".format(Exp_Count)+
                                                        "mov DWORD[{}], eax\n\n".format(temp))
                                        Exp_Count += 1
                                    #This needs to happen at the end.
                                    del postFix[fOI:index + 1]
                                    postFix.insert(fOI,temp)
                                    if(temp4):
                                        temp1 = True
                                        temp2 = False
                                        temp3 = False
                                        temp4 = False
                                    elif(temp3):
                                        temp1 = False
                                        temp2 = False
                                        temp3 = False
                                        temp4 = True
                                    elif(temp2):
                                        temp3 = True
                                        temp1 = False
                                        temp2 = False
                                        temp4 = False
                                    elif(temp1):
                                        temp1 = False
                                        temp2 = True
                                        temp3 = False
                                        temp4 = False

                                    break
                            if(len(postFix) == 1):
                                postFix.pop()
                        #fp.write("got here")
                        if(postFix == []):
                            fo.write("mov eax, DWORD[{}]\n".format(temp)+
                                "mov DWORD[{}], eax\n\n".format(varName))
                    else:
                        fo.write("mov DWORD[{}], {}\n\n".format(varName, rightSide))
            elif(re.search(WRITE_STRING, i)):
                strOut = i.split("\"")[1]

                #print(strOut)
                #check for valid stringvariable ???
                strVarName = VARS["\"{}\"".format(strOut)].split(",")[2]
                fo.write("push {}\n".format(strVarName)+
                                "push stringPrinter\n"+
                                "call _printf\n"+
                                "add esp, 0x08\n\n")

            elif(re.search(WRITE_VAR, i)):
                fo.write("push DWORD[{}]\n".format(i.split(" ")[1][:-1])+
                            "push numberPrinter\n"+
                            "call _printf\n"+
                            "add esp, 0x08\n\n")

            elif(re.search(READ_VAR, i)):
                fo.write("pusha\n"+
                         "push {}\n".format(i.split(" ")[1][:-1])+
                         "push dword int_format\n"+
                         "call _scanf\n"+
                         "add esp, 0x04\n"+
                         "popa\n\n")

            elif(i[0:3] == "for"):
                forStatement = i.split(" ")
                print(forStatement)
                varI = "DWORD[{}]".format(forStatement[1])
                iSetTo = "DWORD[{}]".format(forStatement[3]) if not isInt(forStatement[3]) else forStatement[3]
                toVar = "DWORD[{}]".format(forStatement[5]) if not isInt(forStatement[5]) else forStatement[5]
                stepVar = "DWORD[{}]".format(forStatement[7]) if not isInt(forStatement[7]) else forStatement[7]

                print("{} {} {} {}".format(varI, iSetTo, toVar, stepVar))
                bracketsIn += 1
                firstR = ""
                secondR = ""

                """if(bracketsIn%2==0):
                    firstR = "ecx"
                    secondR = "edx"
                else:
                    firstR = "edx"
                    secondR = "ecx"
                """
                firstR = "ecx"
                secondR = "edx"
                if(not "[" in iSetTo):
                    fo.write("mov {}, {}\n".format(varI, iSetTo)+
                         "mov {}, {}\n".format(firstR, toVar)+
                         "_loop_start_{}:\n".format(forLoopCount)+
                         "cmp {}, {}\n".format(varI, firstR)+
                         "jg _loop_end_{}\n".format(forLoopCount)+
                         "pusha\n\n")
                else:
                    fo.write("mov {}, {}\n".format(firstR, iSetTo)+
                         "mov {}, {}\n".format(varI, firstR)+
                         "mov {}, {}\n".format(firstR, toVar)+
                         "_loop_start_{}:\n".format(forLoopCount)+
                         "cmp {}, {}\n".format(varI, firstR)+
                         "jg _loop_end_{}\n".format(forLoopCount)+
                         "pusha\n\n")

                #fo.write("FOR STATEMTENT '{}'\n\n".format(forLoopCount))
                if(not "[" in stepVar):
                    BLOCK_STACK.append("popa\n"+
                                    "add {}, {}\n".format(varI, stepVar)+
                                   "jmp _loop_start_{}\n".format(forLoopCount)+
                                   "_loop_end_{}:\n\n".format(forLoopCount))
                else:
                    BLOCK_STACK.append("popa\n"+
                                    "mov {}, {}\n".format(secondR, stepVar)+
                                   "add {}, {}\n".format(varI, secondR)+
                                   "jmp _loop_start_{}\n".format(forLoopCount)+
                                   "_loop_end_{}:\n\n".format(forLoopCount))
                forLoopCount += 1
            elif(i[0:2] == "if"):
                ifData = i.split()
                if(len(ifData) == 6):
                    ifData = [ifData[0], ifData[1], ifData[2]+ifData[3], ifData[4], ifData[5]]

                ifJump = getJump(ifData[2])
                if(not isInt(ifData[1]) and not isInt(ifData[3])):
                    fo.write("mov edi, DWORD[{}]\n".format(ifData[1])+
                             "cmp edi, DWORD[{}]\n".format(ifData[3]))
                elif(not isInt(ifData[1]) and isInt(ifData[3])):
                    fo.write("mov edi, DWORD[{}]\n".format(ifData[1])+
                             "cmp edi, {}\n".format(ifData[3]))
                elif(isInt(ifData[1]) and not isInt(ifData[3])):
                    fo.write("mov edi, {}\n".format(ifData[1])+
                             "cmp edi, DWORD[{}]\n".format(ifData[3]))
                elif(isInt(ifData[1]) and isInt(ifData[3])):
                    fo.write("mov edi, {}\n".format(ifData[1])+
                             "cmp edi, {}\n".format(ifData[3]))

                fo.write("{} _endif_{}\n\n".format(ifJump, ifcount))

                if("if{}".format(ifcount) in elseList):
                    BLOCK_STACK.append("jmp _endelse_{}\n".format(ifcount)+
                                       "_endif_{}:\n\n".format(ifcount))
                    ELSE_STACK.append("_endelse_{}:\n\n".format(ifcount))
                else:
                    BLOCK_STACK.append("_endif_{}:\n\n".format(ifcount))

                print(ifcount)
                ifcount += 1
            elif(i[0:4] == "else"):
                BLOCK_STACK.append(ELSE_STACK.pop())
            elif(i[0:6] == "switch"): #SWITCH Blocks
                switchData = i.split(" ") #Split the switch instruction with spaces.
                varName = switchData[1][1:] #Get rid of the first parenthesis in the second token in switch statement.
                varName = varName[:-1] #Get rid of the last parenthesis in the second token in switch statement.
                switchVar = varName  #This switchVar is a global variable which keeps track of the current switch variable.

                #Appendind the ending clause for a switch statement to my blocks stack to be able to print it out once a closing bracket is found.
                BLOCK_STACK.append("_endswitch_{}:\n".format(switchCount))
            elif(i[0:4] == "case"): #CASE Blocks
                caseData = i.split(" ") #Split the case instruction with spaces.
                num = caseData[1][:-1] #Get rid of the ending ':' in the second token in case statement.

                fo.write("mov edi, DWORD[{}]\n".format(switchVar) +
                         "cmp edi, {}\n".format(num)+
                         "jnz _endcase_{}\n".format(caseCount))

                BLOCK_STACK.append("jmp _endswitch_{}\n".format(switchCount) +
                                    "_endcase_{}:\n".format(caseCount))

                caseCount += 1 #Increment Case Count by one to be able to have different ones.
            elif(i[0:7] == "default"): #Default case in switch statements.
                BLOCK_STACK.append("\n")  #If it finds one, dont do anything just print whatever is in block.
                switchCount += 1
            elif(i[0:9] == "procedure"):
                if(procedureCount == maxProcedureCount):
                    fo.write("jmp afterprocedures\n")
                    
                procedureData = i.split(" ")
                procedureName = procedureData[1]
                
                print(procedureName)
                #Writing label name for procedure
                fo.write("{}:\n".format(procedureName))
                BLOCK_STACK.append(";END procedure\n"+
                                   "ret\n\n")
                if(len(procedureData) == 5):
                    procedureVar = procedureData[3] + procedureData[4][:-1]
                else:
                    procedureVar = procedureData[3][:-1]
                print(procedureVar)
                procedureCount -= 1
                procedure = True
            elif(i[0:1] == "}"): #Closing Brackets, AKA Block closed.
                peeked = BLOCK_STACK[-1]
                fo.write(BLOCK_STACK.pop())
                if("procedure" in peeked):
                    procedure = False
                    if(procedureCount == 0):
                        fo.write("afterprocedures:\n")
                
                peeked = ""
                bracketsIn -= 1
            else:#This is where I check if the instruction has the name of one of the procedures, therefore a procedure is being called.
                for n in procedureNames:
                    if(n in i):
                        #For now lets just use passin
                        print("Procedure Found : {}".format(i))
                        passedVariable = i.split("(")[1].strip().replace(" ", "")[:-2]
                        print(passedVariable)
                        if(procedureNames[n] == "value"):
                            fo.write("mov eax, DWORD[{}]\n".format(passedVariable)+
                                "mov DWORD[passin], eax\n" +
                                "call {}\n".format(n)+
                                 "add 	esp, 0x04\n\n")
                        else:
                            fo.write("mov eax, DWORD[{}]\n".format(passedVariable)+
                                "mov DWORD[passin], eax\n" +
                                "call {}\n".format(n)+
                                 "add 	esp, 0x04\n"+
                                 "mov eax, DWORD[passin]\n"+
                                "mov DWORD[{}], eax\n\n".format(passedVariable))
        print(procedureNames)

        fo.write("exit:\n"+
                "; All done.\n"+
	            "mov	eax, 0x0\n"+
	            "call	_ExitProcess@4\n"+
                "; (eof)\n")

####END Run()############

def getJump(op):
    if(op == "=="):
        return "jnz"
    elif(op == "!="):
        return "jz"
    elif(op == ">"):
        return "jle"

def equalsFunction(i):
    instruction = i.split("=")
    instruction[0] = instruction[0].strip()
    instruction[1] = instruction[1].strip()

    if(re.search(SETNUM_EQUALTO,instruction[0])):
        #print("in")
        #if('+' in instruction[1] or '-' in instruction[1] or '*' in instruction[1] or '^' in instruction[1]):
            #inst = re.split('\+|\-|\*|\^', instruction[1].strip()[:-1])
            #for i,j in enumerate(inst):
                #print(j)
        if(not isInt(instruction[1][:-1])):
            VARS[instruction[0].split(" ")[1]] = "u,{}".format(instruction[0].split(" ")[0])
        else:
            VARS[instruction[0].split(" ")[1]] = "i,{},{}".format(instruction[0].split(" ")[0], instruction[1][:-1])

def createSTRVar(i):
    """[creates a variable of type string]

    Args:
        i ([str]): [instruction line]
    """
    global strVarCount
    instruction = i.split("\"")
    varType = "str"
    varName = "\"{}\"".format(instruction[1])
    if(not varName in VARS):
        VARS[varName] = "i,{},s{}".format(varType,strVarCount)
        strVarCount += 1

def createVariable(i):
    instruction = i.split(" ")
    varType = instruction[0]
    varName = instruction[1][:-1]
    if(not varName in VARS):
        VARS[varName] = "u,{}".format(varType)

def isInt(x):
    """[Helper method to check whether the given input is an intger or not]

    Args:
        x (integer): [user input]

    Returns:
        [boolean]: [whether the passed in value is an integer or not]
    """
    try:
        x = int(x)
        return True
    except ValueError:
        return False

def main():
    """[Sets the fileIn and fileOut string to the specified one, checks if there is a file with the fileIn path,
    and runs the run() function by passing both file paths in.]
    """
    fileName = "procedureTry"
    fileIn = "./" + fileName + ".txt"
    fileOut = "./" + fileName + ".asm"

    if not os.path.isfile(fileIn):
        print("File not found")
        sys.exit()
    else:
        run(fileIn, fileOut)

if __name__ == '__main__':
    main()
