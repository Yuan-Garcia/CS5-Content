import re
import inspect  
import ast
from Cyclomatic import *
from NestedDepth import *

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

def findRecursion(scriptPath):
    #split into functions, then find function name within the functions
    #def whitespace word (anything ) colon
    totalScriptList = []
    inputFile = open(scriptPath, "r")
    for x in inputFile:
        totalScriptList.append(x)
    names = funcName(totalScriptList)
    for n, i in enumerate(splitFunc(scriptPath)):
        if i.count(names[n]) > 1:
            return True
    return False


# def findInheritance(fullScript): 


def findListComp(scriptPath):
    """Detect specific list comprehensions in the given script."""
    with open(scriptPath, "r") as file:
        script_code = file.read()

    tree = ast.parse(script_code, filename=scriptPath)

    def is_specific_list_comp(node):
        """Check if the list comprehension matches the specified formats."""
        if isinstance(node.elt, ast.Call) and isinstance(node.elt.func, ast.Name):
            if isinstance(node.generators[0].target, ast.Name) and isinstance(node.generators[0].iter, ast.Name):
                return True
        elif isinstance(node.elt, ast.List) and len(node.elt.elts) == 2:
            if isinstance(node.elt.elts[0], ast.Call) and isinstance(node.elt.elts[1], ast.Name):
                if isinstance(node.generators[0].target, ast.Name) and isinstance(node.generators[0].iter, ast.Name):
                    return True
        return False

    return any(is_specific_list_comp(node) for node in ast.walk(tree) if isinstance(node, ast.ListComp))

    # with open(scriptPath, "r") as file:
    #     tree = ast.parse(file.read(), filename=scriptPath)
    # for node in ast.walk(tree):
    #     if isinstance(node, ast.ListComp):
    #         return True
    # return False
    

def findOop(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    hasClass = False
    hasMethod = False

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            hasClass = True
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    hasMethod = True

    return hasClass and hasMethod


commentList = []
totalScriptList = []

scriptPath = "Brennock.py"

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
  
#print("The comment level is: " + str(len(commentList)))
print("The percentage comments is: " + str((1-(len(noCommentsinputfile)/len(open(scriptPath, "r").read())))*100))

print("There are " + str(len(funcName(totalScriptList))) + " functions present")
#print("These functions are: " + str(funcName(totalScriptList)))

print("The total Cyclomatic Complexity is " + str(calculate_cyclomatic_complexity(open(scriptPath, "r").read())))

call_graph = build_call_graph(scriptPath)
ambition_score = measure_ambition(call_graph)
print("The highest level of function nesting is " + str(ambition_score))

print("Has if's or variables?" ,findIfOrVar(noCommentsinputfile))
print("Has list comprehension?" ,findListComp(scriptPath))
print("Has nested loops?",findNestedLoops(scriptPath))
print("Has recursion?",findRecursion(scriptPath))
#print(findFunctionsInScript("LOC.py"))
#hi


    
# for i, n in enumerate((splitFunc(totalScriptList))):
#     print(n, i)
#print((splitFunc(totalScriptList)))

# testing on LOC.py
#print(removeComments(inputfiletest2.read()))
#print(inputfiletest2.read())
#print(commentCheck(inputfile.read()))


