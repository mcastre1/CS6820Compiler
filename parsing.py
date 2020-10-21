def fixSpacing(InstSTR):
    inst = InstSTR
    if("=" in inst):
        indOcu = inst.find("=")
        if(not inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("=", " = ")
        elif(not inst[indOcu - 1] == " " and inst[indOcu + 1] == " "):
            inst = inst.replace("=", " =")
        elif(inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("=", "= ")
    if("-" in inst):
        indOcu = inst.find("-")
        if(not inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("-", " - ")
        elif(not inst[indOcu - 1] == " " and inst[indOcu + 1] == " "):
            inst = inst.replace("-", " -")
        elif(inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("-", "- ")
    if("+" in inst):
        indOcu = inst.find("+")
        if(not inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("+", " + ")
        elif(not inst[indOcu - 1] == " " and inst[indOcu + 1] == " "):
            inst = inst.replace("+", " +")
        elif(inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("+", "+ ")
    if("*" in inst):
        indOcu = inst.find("*")
        if(not inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("*", " * ")
        elif(not inst[indOcu - 1] == " " and inst[indOcu + 1] == " "):
            inst = inst.replace("*", " *")
        elif(inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("*", "* ")
    if("^" in inst):
        indOcu = inst.find("^")
        if(not inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("^", " ^ ")
        elif(not inst[indOcu - 1] == " " and inst[indOcu + 1] == " "):
            inst = inst.replace("^", " ^")
        elif(inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("^", "^ ")
    if("(" in inst and not "switch" in inst and not "procedure" in inst): #Had to add not switch because it will normally end with a ) therefor I cant look forward. 
        indOcu = inst.find("(")
        if(not inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("(", " ( ")
        elif(not inst[indOcu - 1] == " " and inst[indOcu + 1] == " "):
            inst = inst.replace("(", " (")
        elif(inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace("(", "( ")
    if(")" in inst and not "switch" in inst and not "procedure" in inst):
        indOcu = inst.find(")")
        if(not inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace(")", " ) ")
        elif(not inst[indOcu - 1] == " " and inst[indOcu + 1] == " "):
            inst = inst.replace(")", " )")
        elif(inst[indOcu - 1] == " " and not inst[indOcu + 1] == " "):
            inst = inst.replace(")", ") ")
    
    return inst

def removeComments(line, mc):
    mc = mc
    if(not line == ""):
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
            INSTRUCTIONS.append(lineN)