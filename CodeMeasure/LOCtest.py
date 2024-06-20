import re
import inspect  
import ast 

def commentCheck(comment): #fix becauyse it works now
    #hashtags = "\#[^\n\r]+?(?:[\n\r])"   # is the actual solution
    hashtags = "[\#]" # is the very temporary solution until I figure out how to get the actual solution to work
    if re.search(hashtags, comment):
        return comment
    else:
        return ""
    #print(commentCheck("#will this work"))
    #print(commentCheck("we will see"))

# def CyclomaticChicanery(noCommentScriptStr):
#     wordScript = noCommentScriptStr.split(" ")
#     addOne = "for|if|for|while|except|with|assert| in |and|or|not|implies" # add more list comprehensions
#     CyclomaticCount = 0
#     for i in wordScript:
#         if re.search(addOne, i): # if it's in the checkers then decrement the cyclomatic count :)
#             CyclomaticCount = CyclomaticCount + 1
#     return CyclomaticCount

def removeComments(fullScript):
    multiLine = "\'\'\'[^']*\'\'\'|\"\"\"[^\"]*\"\"\"" # gets all docstrings
    fullScript = re.sub(multiLine, "", fullScript) # replaces all docstrings with an emptystring
    fullScript = re.sub("#.*","",fullScript) #replaces everything that has a comment with an emptystring
    return fullScript

def findFunctionsInScript(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions

def getFunctionSource(scriptPath, func_node):
    with open(scriptPath, "r") as file:
        lines = file.readlines()

    start_line = func_node.lineno - 1
    end_line = func_node.end_lineno

    return "".join(lines[start_line:end_line])

def splitFunc(scriptPath):
    funcList = []
    functions = findFunctionsInScript(scriptPath)
    for func in functions:
        funcList.append(getFunctionSource(scriptPath, func))
    return funcList

def funcName(fullScript):
    tempList = []
    ansList = []
    getNames = "(def +[a-zA-Z_]+( [^(]+)*)" #gets only the def (name)
    for i in fullScript:
        if re.search(getNames, i):
            tempList.append(i)
    for n, i in enumerate(tempList):
        ansList.append((i.split("(")[0])[4:]) #parses out the variable and the "def ", giving only the variable name
    return ansList

def containsString(str, noCommentScriptStr):
    wordScript = noCommentScriptStr.split(" ")
    for i in wordScript:
        if re.search(str, i):
            return True
    return False

def findIfOrVar(noCommentScriptStr):
    return containsString("if|=", noCommentScriptStr)

def findBoolAlg(noCommentScriptStr):
    return containsString("and|or|not|", noCommentScriptStr)

def findDictionaries(noCommentScriptStr):
    return containsString( "\{(?:[^{}]|(?R))*\})", noCommentScriptStr)

def findSlicing(noCommentScriptStr):
    return containsString("\[.*:.*\]", noCommentScriptStr)

def findNestedLoops(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.For, ast.While)):
                    return True

def findRecursion(noCommentScripStr):
    #split into functions, then find function name within the functions
    #def whitespace word (anything ) colon
    funcNames = "def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):" # maps everything from after def to before colon
    funcBlocks = " " # takes the body of the function
    #loop thru funcBlocks to see where funcNames align?

#def findLoops(fullScript):
    #for loop pattern:  for\s+\w+\s+in\s+.+:     (only retrieves the header, not the body of the loop yet)
    # while loop header pattern: while\s+.+:


# def findInheritance(fullScript): 


def findListComp(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)
    for node in ast.walk(tree):
        if isinstance(node, ast.ListComp):
            return True
    return False



commentList = []
totalScriptList = []

scriptPath = "LOC.py"

inputfile = open(scriptPath, "r")
inputfiletest2 = open(scriptPath, "r")
noCommentsinputfile = removeComments(inputfiletest2.read())
for x in inputfile:
    totalScriptList.append(x)
    commentList.append(commentCheck(x))

for i in splitFunc(scriptPath):
    print(i)

commentList = [z for z in commentList if z != ""]
print("The total LOC is: " + str(len(totalScriptList)))
#print("The Cyclomatic Complexity is: " + str(CyclomaticChicanery(noCommentsinputfile)))
  
print("The comment level is: " + str(len(commentList)))
print("The percentage comments is: " + str((len(commentList)/len(totalScriptList))*100))
print("There are " + str(len(funcName(totalScriptList))) + " functions present")
print("These functions are: " + str(funcName(totalScriptList)))
print("Are there if's or variables? " + str(findIfOrVar(noCommentsinputfile)))

#print(splitFunc(scriptPath))
# print(inspect.getsource(funcName))

print("Has list iteration?: " ,findListComp("LOC.py"))
print("Has nested loops?",findNestedLoops("LOC.py"))
#print(findFunctionsInScript("LOC.py"))
#hi


    
# for i, n in enumerate((splitFunc(totalScriptList))):
#     print(n, i)
#print((splitFunc(totalScriptList)))

# testing on LOC.py
#print(removeComments(inputfiletest2.read()))
#print(inputfiletest2.read())
#print(commentCheck(inputfile.read()))


