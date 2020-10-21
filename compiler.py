import sys
import os
import re
from shutil import copy
import cPostFix

errors = []
uninitializedVariables = {}
initializedVariables = {}
instructions = []
imports = []

def main():
    
    #Path to our BOBBALL source code.
    fileName = "arrayStatement.txt"
    filepath = "./" + fileName
    lineCount = 0
    expCounter = 0
    multiblockCount = 0
    outStringCounter = 0
    error = False

    #initializedVariables["num2"] = 32
    #Check if file exists in system.
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    #Count the number of lines in source file.
    with open(filepath) as fp:
        for line in fp:
            lineCount += 1
    
    #Check for syntax errors.
    with open(filepath) as fp:
        cnt = 1
        commentBlock = False
        
        #Iterate through each line in the opened file. 
        for line in fp:
            error = False
            line = line.lstrip()
            
            #if(line[:2] == "/*"):
            if("/*" in line):
                commentBlock = True
                multiblockCount += 1
            
            #Checking if line doesn't start with a comment. 
            if(line[:2] != "//" and not commentBlock): 
                #Makes sure the source file starts with program "name";           
                if(cnt == 1):
                    if not (re.search("^program\s\w+;$", line)):
                        error = True
                        errors.append("Error at beginning of program, should start with program 'name';")
                #Makes sure that the second line after program, is begin.
                elif(cnt == 2):
                    if not (re.search("^begin$", line)):  #This is one is taking into consideration a tab, might need to do it so it doesnt care about whitespace.
                        error = True
                        errors.append("'begin' expected at line {}".format(cnt))
                elif(cnt == lineCount):
                    if not (re.search("^end.$", line)):
                        error = True
                        errors.append("'end.' expected at line {}".format(cnt))
                #Checks for missing semicolons in every instruction.
                elif not (re.search(";$",line)):
                    if not ("//" in line):
                        error = True
                        errors.append("Error at line {}, missing semicolon".format(cnt))
                            
                
                #Add regex for checking for comments after ; in an instruction/statement.
                if not (error):
                    #Check for initialized variables.                  
                    #This one checks for straight forward initialization, such as num num1 = 2;
                    if (re.search("^num\s[A-Za-z0-9]+\s?=\s?[0-9];$",line)):
                        stringInput = line.lstrip().split("=")
                        if not stringInput[0].split(" ")[1] in initializedVariables:
                            p = re.compile("[0-9]+")
                            result = p.search(stringInput[1].lstrip())   
                            initializedVariables[stringInput[0].split(" ")[1]] = result.group(0)
                    elif(re.search("num\s[A-Za-z0-9]+;\s*", line)):
                        stringInput = line.lstrip().split(" ")
                        p = re.compile("[A-Za-z0-9]+")
                        result = p.search(stringInput[1])
                        if not stringInput[0] in uninitializedVariables:
                            uninitializedVariables[result.group(0)] = "num"
                    elif(re.search("num\s[A-Za-z0-9]+\s?=\s?.+;\s*", line)):
                        stringInput = line.lstrip().split("=")
                        if not stringInput[0].split(" ")[1] in uninitializedVariables:
                            p = re.compile("[A-Za-z0-9]+")
                            print(stringInput[1])  
                            if("*" in stringInput[1] or "+" in stringInput[1] or "-" in stringInput[1] or "^" in stringInput[1] or "/" in stringInput[1]):
                                print("GOT HERE")
                                p = re.compile("\\w(?:\\s[)(+*^-]\\s\\w)+")
                                result = p.search(stringInput[1])
                                print(stringInput[0].split(" ")[1])
                                uninitializedVariables[stringInput[0].split(" ")[1]] = "ae"
                            else:             
                                print("here")             
                                result = p.search(stringInput[1])                                                        
                                uninitializedVariables[stringInput[0].split(" ")[1]] = result.group(0)
                            
                        if(re.search("[A-Za-z0-9]+\s?=\s?\\w(?:\\s[)(+*^-]\\s\\w)+", line)):
                            instructions.append(line.lstrip().rstrip()) 
                    elif(re.search("array\s\w+\[(\-?\d+\.\.\-?\d+\,|\-?\d+\.\.\-?\d+)+\]\;", line)):
                        stringInput = line.lstrip().rstrip().split(" ")
                        variableName = stringInput[1].split("[")[0]
                        #ARRAY
                        #print("stringInput {} {}".format(stringInput[0], stringInput[1]))
                        #print(variableName)
                        
                        if not variableName in uninitializedVariables:
                            uninitializedVariables[variableName] = "array " + stringInput[1]
                            
                    
                    #Check for instructions  
                    elif(re.search("[A-Za-z0-9]+\s?=\s?.+", line)): #If for variable initialization, nums.
                        instructions.append(line.lstrip().rstrip()) 
                    elif(re.search("\w+\[.+\]\s?=\s?.+\;", line)): #If for array instructions.
                        instructions.append(line.lstrip().rstrip())
                    elif(re.search("write\s.+", line)):  #If for write instructions.
                        if(re.search("\".+\"",line.split(" ")[1].lstrip().rstrip())):
                            if not (line.split(" ")[1] in initializedVariables):
                                p = re.compile(".+(?!;).*")
                                result = p.search(line.split(" ")[1].rstrip().lstrip())
                                initializedVariables["s{}".format(outStringCounter)] = result.group(0)[:-1] + ",0x0d,0x0a,0"
                                outStringCounter += 1
                                
                            ##TODO########################################################################################
                            #Check if the stringPrinter is being used already, if not add it.
                            
                        #This part checks to see if there is a _printf in our imports list. 
                        if not ("_printf" in  imports):
                            imports.append("_printf")
                        if not("stringPrinter" in  initializedVariables):
                                initializedVariables["stringPrinter"] = "stringPrinter " + "db \"%s\",0"
                        if not("numberPrinter" in initializedVariables):
                                initializedVariables["numberPrinter"] = "numberPrinter " + "db \"%d\",0x0d,0x0a,0"
                        #Adds the whole instruction to the instructions list, which will later be used to print to an asm file.
                        instructions.append(line.lstrip().rstrip())
                                          
            #Checks for multi line comments. 
            elif commentBlock:
                if "*/" in line:
                    commentBlock = False
                    multiblockCount -= 1
  
            cnt += 1
    
    #print("MLBC = {}".format(multiblockCount))
    if not (multiblockCount == 0):
        error = True
        errors.append("MultiLine comment not closed")
    #If there are errors do something here.
    if(error):     
        print("Found error...")
        errorOutputFile = "./basics.err"
        print("Errors found, please check the directory: {} ".format(errorOutputFile))   
        with open(errorOutputFile, "w+") as fp:
            for e in errors:
                fp.write(e)
        
    
    #Output file path
    outputFilePath = "./basics.asm"
    
    #Writing out to the ouptput file
    with open(outputFilePath, "w+") as fp:
        fp.write(";-----------------------------\n"+
                "; exports\n"+
                ";-----------------------------\n"+
                "global _main\n"+
                "EXPORT _main\n"+
                "\n")
        
        
        fp.write(";-----------------------------\n"+
                "; imports\n"+ 
                ";-----------------------------\n"+
                "extern _ExitProcess@4\n")
        
        for imp in imports:
            fp.write("extern {}\n".format(imp))
            
        fp.write("\n"+
                ";-----------------------------\n"+
                "; initialized data\n"+ 
                ";-----------------------------\n"+
                "section .data USE32\n")    
        
    
        for d in initializedVariables:
            if(initializedVariables[d].isnumeric()):
                fp.write(d + " dd " + initializedVariables[d] + "\n")
            elif(initializedVariables[d].startswith("\"")):
                fp.write(d + " db " + initializedVariables[d] + "\n")
            else:
                fp.write(initializedVariables[d]+"\n")
                
        fp.write("\n")
        #fp.write("s0	db \"Basics.txt:\",0x0d,0x0a,0\n")
        #fp.write("stringPrinter	db \"%s\",0\n")
        #fp.write("numberPrinter	db \"%d\",0x0d,0x0a,0\n\n")
        fp.write(";-----------------------------\n"+
                 "; uninitialized data\n"+ 
                 ";-----------------------------\n"+
                 "section .bss USE32\n" +
                 "temp resd 1\n"+
                 "temp2 resd 1\n"+
                 "temp3 resd 1\n"+
                 "temp4 resd 1\n")

        for d in uninitializedVariables:
            if(uninitializedVariables[d].split(" ")[0] == "array"):
                numbers = uninitializedVariables[d].split(" ")[1].split("[")[1]
                numbers = numbers[:-2]
                size = 1
                if("," in numbers):
                    numberList = numbers.split(",")
                    for i in numberList:
                        temp = i.split("..")
                        size = size * (int(temp[1]) - int(temp[0]) + 1)
                    size = size * 4
                    fp.write("{} resb {}\n".format(d, size))
            else:
                    fp.write(d + " resd 1\n")
            
    
        fp.write("\n")
        fp.write(";-----------------------------\n"+
                 "; Code! (execution starts at _main\n"+ 
                 ";-----------------------------\n"+
                 "section .code USE32\n\n"+
                 "_main:\n\n")
        
        for i in uninitializedVariables:
            if not (uninitializedVariables[i] == "num"):
                if(uninitializedVariables[i] in initializedVariables or uninitializedVariables[i] in uninitializedVariables):
                    fp.write("mov edi, DWORD["+uninitializedVariables[i]+"]\n"+
                             "mov DWORD["+i+"], edi\n")
    
        #Go through all instructions.
        for i in instructions:
            if(re.search(".+=.+", i)):
                variable = i.split("=")[0].lstrip().rstrip()

                #If instruction is arithmetic expression, do this.
                if(re.search("\\w(?:\\s[)(+*^-]\\s\\w)+", i.split("=")[1])):
                    global pf
                    inst = i.split("=")[1].rstrip().lstrip()[:-1]
                    inst = inst.replace("(", "( ")
                    inst = inst.replace(")", " )")
                    pf = cPostFix.infixToPostfix(inst)
                    operators = ['-', '+', '*', '/', '^']
                    temp1 = False
                    temp2 = False
                    temp3 = False
                    temp4 = False
                    
                    while(not len(pf) == 0):
                        #print(variable)
                        if(len(variable.split(" ")) == 2):
                            #print("HERE")
                            variable = variable.split(" ")[1]
                        for index, v in enumerate(pf):
                            if(v in operators):
                                fOI = index - 2
                                sOI = index - 1
                                print("found operator {}, combo: {}{}{}".format(v, pf[fOI],v,pf[sOI]))
                                
                                #Very bad way of keeping track of temp variables, I should probably make a list and check like that. 
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
                                    
                                #Here's where I'll start checking for operators:
                                if(v == '*'):
                                    if(isInt(pf[fOI])):
                                        if(isInt(pf[sOI])):
                                            fp.write("mov edi, {}\n".format(pf[fOI])+
                                                "imul edi, {}\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            fp.write("mov edi, {}\n".format(pf[fOI])+
                                                "imul edi, DWORD[{}]\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                    else:
                                        if(isInt(pf[sOI])):
                                            fp.write("mov edi, DWORD[{}]\n".format(pf[fOI])+
                                                "imul edi, {}\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            fp.write("mov edi, DWORD[{}]\n".format(pf[fOI])+
                                                "imul edi, DWORD[{}]\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                            
                                elif(v == '+'):
                                    if(isInt(pf[fOI])):
                                        if(isInt(pf[sOI])):
                                            fp.write("mov edi, {}\n".format(pf[fOI])+
                                                "add edi, {}\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            fp.write("mov edi, {}\n".format(pf[fOI])+
                                                "add edi, DWORD[{}]\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                    else:
                                        if(isInt(pf[sOI])):
                                            fp.write("mov edi, DWORD[{}]\n".format(pf[fOI])+
                                                "add edi, {}\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            fp.write("mov edi, DWORD[{}]\n".format(pf[fOI])+
                                                "add edi, DWORD[{}]\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                    
                                elif(v == '-'):
                                    if(isInt(pf[fOI])):
                                        if(isInt(pf[sOI])):
                                            fp.write("mov edi, {}\n".format(pf[fOI])+
                                                "sub edi, {}\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            fp.write("mov edi, {}\n".format(pf[fOI])+
                                                "sub edi, DWORD[{}]\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                    else:
                                        if(isInt(pf[sOI])):
                                            fp.write("mov edi, DWORD[{}]\n".format(pf[fOI])+
                                                "sub edi, {}\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                        else:
                                            fp.write("mov edi, DWORD[{}]\n".format(pf[fOI])+
                                                "sub edi, DWORD[{}]\n".format(pf[sOI])+
                                                "mov DWORD[{}], edi\n\n".format(temp))
                                            
                                elif(v == '^'):
                                    if(isInt(pf[fOI])):
                                        if(isInt(pf[sOI])):
                                            fp.write("xor edi, edi\n"+
                                                     "mov eax, 0x00000001\n"+
                                                     "_exp_top_{}:\n".format(expCounter)+
                                                     "cmp edi, {}\n".format(pf[sOI])+
                                                     "jz _exp_out_{}\n".format(expCounter)+
                                                     "imul eax, {}\n".format(pf[fOI])+
                                                     "inc edi\n"+
                                                     "jmp _exp_top_{}\n".format(expCounter)+
                                                     "_exp_out_{}:\n".format(expCounter)+
                                                     "mov DWORD[{}], eax\n\n".format(temp))
                                        else:
                                            fp.write("xor edi, edi\n"+
                                                     "mov eax, 0x00000001\n"+
                                                     "_exp_top_{}:\n".format(expCounter)+
                                                     "cmp edi, DWORD[{}]\n".format(pf[sOI])+
                                                     "jz _exp_out_{}\n".format(expCounter)+
                                                     "imul eax, {}\n".format(pf[fOI])+
                                                     "inc edi\n"+
                                                     "jmp _exp_top_{}\n".format(expCounter)+
                                                     "_exp_out_{}:\n".format(expCounter)+
                                                     "mov DWORD[{}], eax\n\n".format(temp))
                                    else:
                                        if(isInt(pf[sOI])):
                                            fp.write("xor edi, edi\n"+
                                                     "mov eax, 0x00000001\n"+
                                                     "_exp_top_{}:\n".format(expCounter)+
                                                     "cmp edi, {}\n".format(pf[sOI])+
                                                     "jz _exp_out_{}\n".format(expCounter)+
                                                     "imul eax, DWORD[{}]\n".format(pf[fOI])+
                                                     "inc edi\n"+
                                                     "jmp _exp_top_{}\n".format(expCounter)+
                                                     "_exp_out_{}:\n".format(expCounter)+
                                                     "mov DWORD[{}], eax\n\n".format(temp))
                                        else:
                                            fp.write("xor edi, edi\n"+
                                                     "mov eax, 0x00000001\n"+
                                                     "_exp_top_{}:\n".format(expCounter)+
                                                     "cmp edi, DWORD[{}]\n".format(pf[sOI])+
                                                     "jz _exp_out_{}\n".format(expCounter)+
                                                     "imul eax, DWORD[{}]\n".format(pf[fOI])+
                                                     "inc edi\n"+
                                                     "jmp _exp_top_{}\n".format(expCounter)+
                                                     "_exp_out_{}:\n".format(expCounter)+
                                                     "mov DWORD[{}], eax\n\n".format(temp))
                                    expCounter += 1
                                #This needs to happen at the end.               
                                del pf[fOI:index + 1]
                                pf.insert(fOI,temp)
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
                        
                        if(len(pf) == 1):
                            pf.pop()
                        #fp.write("got here")
                        if(pf == []):
                            fp.write("mov eax, DWORD[{}]\n".format(temp)+
                                "mov DWORD[{}], eax\n\n".format(variable))

                if(re.search("\w+\[.+\]\s?=\s?.+\;", i)): #Here we write the correct asm for each time we set a data cell in our array.
                    ks = []  #Ks for each of the index bounds
                    deltas = [] #deltas for each index
                    lowerBounds = [] #lowerbounds of index, first number
                    variable = i.split("=")[0].lstrip().rstrip().split("[")[0] #Keeps track of the variable name we are accessing.
                    value = i.split("=")[1].lstrip().rstrip().split(";")[0] #Keeps track of the value we are putting into the variable.
                    
                    #If the variable we are currently working with is found in one of our uninitialiazedVariable lists then proceed and set the array index to the value.
                    if variable in uninitializedVariables:
                        
                        ks = findKs(variable)
                        lowerBounds = findLowerBounds(variable)
                        deltas = findDeltas(ks)

                        fp.write("xor edi, edi\n")
                        indexes = i.split("=")[0].lstrip().rstrip().split("[")[1][:-1].split(",")
                        
                        for n in range(len(indexes)):
                            fp.write("mov esi, {}\n".format(deltas[n])+
                                     "imul esi, {}\n".format(indexes[n])+
                                     "add edi, esi\n")
                        
                        reference = 0
                        for r in range(len(indexes)):
                            reference = reference + int(indexes[r]) * int(deltas[r])
    
                        #Relocation Factor
                        #Lower bound is the first number in (#)..# and then the delta
                        #Formula is lowerbound * delta both should be in the same array index 0 lowerbound * 0 delta + 1 lowerbound * 1 delta, and so on.
                        relFactor = findFactors(deltas, lowerBounds)
                        offset = reference - relFactor      

                        fp.write("sub edi, {}\n".format(relFactor)+
                                 "imul edi, 4\n"+
                                 "add edi, {}\n".format(variable)+
                                 "mov	DWORD[edi],	{}\n".format(value))
                        
            elif(re.search(".+\s.+", i)): #This will also match the ones above, need a better way of handling it... oops
                #print("INDISE")
                leftSide = i.split(" ")[0].lstrip().rstrip()
                rightSide = i.split(" ")[1].lstrip().rstrip()
                rightSide = rightSide[:-1]
                
                #print("L:{}".format(leftSide) + "\nR:{}".format(rightSide))
                if((rightSide in uninitializedVariables or rightSide in initializedVariables) and leftSide == "write"):
                    fp.write("push DWORD["+rightSide+"]\n"+
                            "push numberPrinter\n"+
                            "call _printf\n"+
                            "add esp, 0x08\n\n")
                elif(re.search("\".+\"",rightSide)):
                    fp.write("push s0\n"+
                            "push stringPrinter\n"+
                            "call _printf\n"+
                            "add esp, 0x08\n\n")                    
                elif(re.search("\w+\[.+\]",rightSide)): #This if statement will occur if the instruction is not an assignment.
                    variableName = rightSide.split("[")[0] #Keeps track of the variable we are working with.
                    print(variableName)
                    for vN in uninitializedVariables:
                        print(vN)
                    if(variableName in uninitializedVariables or variableName in initializedVariables): #Check to make sure we actually have this variable in the system.
                        ks = []  #Ks for each of the index bounds
                        deltas = [] #deltas for each index
                        lowerBounds = [] #lowerbounds of index, first number
                        
                        ks = findKs(variableName)
                        lowerBounds = findLowerBounds(variableName)
                        deltas = findDeltas(ks)
                        relFactor = findFactors(deltas, lowerBounds)
                        
                        fp.write("xor edi, edi\n")
                        indexes = rightSide.split("[")[1][:-1].split(",")
                        for n in range(len(indexes)):
                            fp.write("mov esi, {}\n".format(deltas[n])+
                                     "imul esi, {}\n".format(indexes[n])+
                                     "add edi, esi\n")
                            
                        fp.write("sub edi, {}\n".format(relFactor)+
                                 "imul edi, 4\n"+
                                 "add edi, {}\n".format(variableName)+
                                 "push	DWORD[edi]\n"+
                                 "push numberPrinter\n"+
                                 "call _printf\n"+
                                 "add esp, 0x08\n")
                    else:
                        print("Variable: {}, not found in system".format(variableName))  
                        
        #End of file footer.
        fp.write("\nexit:\n\n"+
                 "; All done.\n"+
	             "mov	eax, 0x0\n"+
	             "call	_ExitProcess@4\n\n"+
                 "; (eof)\n")
        
def findKs(v):
    """findKs will return a list with all the ks found through an array variable."""
    temp = []
    for j in uninitializedVariables[v].split(" ")[1].split("[")[1][:-2].split(","):
        num1 = j.split("..")[0]
        num2 = j.split("..")[1]
        temp.append(int(num2)-int(num1) + 1)
    return temp

def findDeltas(ks):
    """findDeltas will return the delta values calculated with the help of ks"""
    tempList = []
    for x in range(len(ks)):
        temp = 1
        for y in range(x+1, len(ks)):
            temp = temp * ks[y]
        tempList.append(temp)
    return tempList

def findFactors(deltas, lowerBounds):
    """findFactors will calculate and return the factor number using deltas and lowerBounds"""
    relFactor = 0
    for dn in range(len(deltas)):
        relFactor = relFactor + int(deltas[dn]) * int(lowerBounds[dn])
    return relFactor

def findLowerBounds(v):
    """findLowerBounds will retrieve and return a list of all indexes being accessed in an array such as 1, 2, 3 from array[1,2,3]"""
    temp = []
    for j in uninitializedVariables[v].split(" ")[1].split("[")[1][:-2].split(","):
        num = j.split("..")[0]
        temp.append(num)
    return temp

def isInt(x):
    try:
        x = int(x)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    main()