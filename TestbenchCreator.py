import re 
from random import randint
from itertools import chain
"""File Content"""
def RmvSpaces(ContentList): #removes blank spaces of a list ['',1,2] -> [1,2]
    if (type(ContentList) != str): #sometimes a string pass through, we check the case to prevent an error
        while ("" in ContentList):
            ContentList.remove("")
        return ContentList #return the list without blank spaces
    else:
        return ContentList #return the string given

"""File Content"""
def SeparateIO(NewContent):
    rgx= r"(\n)*(input|output)"
    return (re.sub(rgx,r"\n \2",NewContent))

"""File Content """
def RmvComments(FileContentComments):
    rgxcomments = r"((\/\*[,\w\s\'\/\W\[\r\n\*]*\*\/)|(\/\/[\w\']*(.+(?=\n))))"
    return (re.sub(rgxcomments,"",FileContentComments))

"""File Content"""
def findPattern(ContentList, Case, GroupNum): #gives a list that fits with the regex pattern given
    Detected = []
    if(Case == "input"):
        rgx= r"((input)\s*(logic|reg)*\s*(\[\d+:\d+\]|\s*)\s*([\w\s,]*))"
    if(Case == "output"):
        rgx= r"((output)\s*(logic|reg)*\s*(\[\d+:\d+\]|\s*)\s*([\w_\s,]*))"
    if(Case == "module"):
        rgx = r"module\s+([a-zA-Z]\w*)"
    for i in range(0,len(ContentList)):
        if(re.search(rgx, ContentList[i])):
            Detected.append(re.search(rgx, ContentList[i]).group(GroupNum)) #adds the element found, we can specify the group
    
    return Detected #returns a list with all the elements found

"""File Content"""
def splitVar(ContentList):
    rgx=r",\s*;*"
    template=['out','']
    for I in range(0,len(ContentList)):
        if (re.search(rgx,ContentList[I])):
            ContentList[I] = (re.sub(rgx," ",ContentList[I])).split(" ")
        else:
            template[0] =ContentList[I]
            ContentList[I] = template
            template=['out','']
        ContentList[I] = RmvSpaces(ContentList[I])
    return RmvSpaces(ContentList)

"""File Content"""
def numsize(ContentList): #funcion para sacar el tamaño de las entradas y salidas
    rgx=r"(\[(\d+):(\d+)\])"
    x=[]
    for i in ContentList:
        if i == "":
            x.append(int(1))
        else:
            y=re.match(rgx,i)
            x.append(abs(int(y[2])-int(y[3]))+1)
    return x    

"""File Content""""
def subPatterns(ContentList):
    paramDict ={}
    paramkeys = []
    TempList = []
    rgxparam = "((paramete)\s*([\w]*)\s*=\s*([\w']*))"
    for i in ContentList:
        if(re.search(rgxparam,i)):
            paramDict[(re.search(rgxparam,i)).group(3)] = (re.search(rgxparam,i)).group(4)
            paramkeys.append((re.search(rgxparam,i)).group(3)) 

    for i in ContentList: 
        for key in paramkeys: 
            if(re.search(key,i)):
                element = re.sub(key, paramDict[key], i)
        TempList.append(i)
    return TempList;

"""Testbenc Template"""
def writeTB(ModuleName, Inputs, InputSize, Outputs, OutputSize, Timescale, Delays,isSec, ClksName, Reset, RstName):
    tb_file = open("TestBenchFile.txt","w") 
    s='_tb, '
    flatten_list =[]

    tb_file.write(f"//Testbench code \ntimescale {Timescale} \n\n module {ModuleName[0]}_tb;\n")
    tb_file.write("//Input and Outputs\n")

    for i in range (len(Inputs)):
        tb_file.write(f"reg {InputSize[i]} {s.join(Inputs[i])}_tb;\n")
        
    for i in range (len(Outputs)):
        tb_file.write(f"wire {OutputSize[i]} {s.join(Outputs[i])}_tb;\n")
        
    tb_file.write(f"\n\n{ModuleName[0]} UUT(")
    flatten_list.append( list(chain.from_iterable(Inputs)))
    flatten_list.append(list(chain.from_iterable(Outputs)))
    flatten_list = list(chain.from_iterable(flatten_list))
    
    for i in range(len(flatten_list)-1):
        tb_file.write(f".{flatten_list[i]}({flatten_list[i]}_tb), ")

    tb_file.write(f".{flatten_list[len(flatten_list)-1]}({flatten_list[len(flatten_list)-1]}_tb));")
    tb_file.write (f"\ninitial \n\tbegin \n\t\t$dumpfile(\"{ModuleName[0]}tb.vcd\");")
    tb_file.write(f"\n\t\t$dumpvars(1,{ModuleName[0]}_tb); \n\t\t//Suggested Code \n/* ")
    
    intSizes = numsize(InputSize)
    flatInputs = list(chain.from_iterable(Inputs))
    
    if(Reset == "Active High"):
        tb_file.write(f"\t\t{RstName}_tb= 0; //Reset\n")

    if(Reset == "Active Low"):
        tb_file.write(f"\t\t{RstName}_tb = 1 //Reset\n")

    for i in range(len(flatInputs)):
        if (flatInputs[i] != ClksName and flatInputs[i] != RstName):
            tb_file.write(f"\t\t{flatInputs[i]}_tb = 0;\n")
    
    Rstflag = 0
    #ciclo para la escitura de 5 pruebas aleatorias 
    for j in range (0,int(Delays)):
        i=0
        tb_file.write("\n\n\t\t#1\n")
        for items in Inputs:
            for word in items:
                if (word != ClksName and word != RstName):
                    if (Rstflag ==0):
                        if Reset == "Active High":
                            tb_file.write(f"\t\t{RstName}_tb = 1; //Reset\n")
                            Rstflag+=1
                        if Reset == "Active Low":
                            Rstflag+=1
                            tb_file.write(f"\t\t{RstName}_tb = 0; //Reset\n")
                    rand=randint(0,(2**(intSizes[i])-1))
                    rand=str(bin(rand))
                    tb_file.write(" \t\t"+word+"_tb = "+str(intSizes[i])+"'"+rand[1:]+";"+"\n")   
            i=i+1
       
    tb_file.write("*/\n")
    tb_file.write("\t\t#1\n\t\t$finish \n \tend")
    if(ClksName != ""):
        tb_file.write(f"\n\t//Autogenerated Clock with the name {ClksName}_tb\n")
        tb_file.write(f"\talways forever #1 {ClksName}_tb = ~{ClksName}_tb;\n")
    tb_file.write("\n endmodule")
    tb_file.close()

"""Testbench Template"""
def writeError():
    tb_file = open("TestBenchFile.txt","w") 
    tb_file.write("\n\nError!!!!\n\nRevise su codigo.\n\nPudo haber faltado alguna palabra (inputs| outputs| inouts| module).") 
    tb_file.close() 

"""Input File""" 
def giveGUIinfo(Text, Timescale, Delays, isSec,ClksName, Reset, RstName):
    #Archivo a leer
    FileContent = Text
    #print("--------------Original--------------")
    #print(FileContent)
    
    #print("---------------No Comments----------------")
    NewContent =RmvComments(FileContent)
    NewContent = SeparateIO(NewContent)
    #print (NewContent)

    #print(NewContent)
    ContentList = RmvSpaces(NewContent.split("\n"))

    ContentList = subPatterns(ContentList);
    try:
    #Gruop 0 -> Todo, Grupo 1 -> Nombre del Modulo
        #print("---------------Module Name----------------")
        moduleName =findPattern(ContentList,"module",1)
        #print(findPattern(ContentList,"module",1))

        #Grupo 1 -> Todo, Grupo 2 y 3 -> "input" y "reg|logic", Grupo4  -> Tamaño, Grupo 5 ->  Variables
        #print("---------------Input Info----------------")
        InputsList =splitVar(findPattern(ContentList,"input",5))
        InputsSize =findPattern(ContentList,"input",4)
        #print(InputsList)
        #print(InputsSize)

        #print("---------------Output Info----------------")
        OutputsList =splitVar(findPattern(ContentList,"output",5))  
        OutputsSize =findPattern(ContentList,"output",4)
        #print(OutputsList)
        #print(OutputsSize)

        writeTB(moduleName,InputsList,InputsSize,
                OutputsList,OutputsSize, Timescale,
                Delays,isSec,ClksName,Reset, RstName)
    except:
        writeError()