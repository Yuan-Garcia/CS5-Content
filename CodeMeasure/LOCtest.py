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

def CyclomaticChicanery(noCommentScriptStr):
    wordScript = noCommentScriptStr.split(" ")
    addOne = "for|if|for|while|except|with|assert| in |and|or|not|implies" # add more list comprehensions
    CyclomaticCount = 0
    for i in wordScript:
        if re.search(addOne, i): # if it's in the checkers then decrement the cyclomatic count :)
            CyclomaticCount = CyclomaticCount + 1
    return CyclomaticCount

def removeComments(fullScript):
    multiLine = "\'\'\'[^']*\'\'\'|\"\"\"[^\"]*\"\"\"" # gets all docstrings
    fullScript = re.sub(multiLine, "", fullScript) # replaces all docstrings with an emptystring
    fullScript = re.sub("#.*","",fullScript) #replaces everything that has a comment with an emptystring
    return fullScript

def find_functions_in_script(script_path):
    with open(script_path, "r") as file:
        tree = ast.parse(file.read(), filename=script_path)

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions

def get_function_source(script_path, func_node):
    with open(script_path, "r") as file:
        lines = file.readlines()

    start_line = func_node.lineno - 1
    end_line = func_node.end_lineno

    return "".join(lines[start_line:end_line])

def splitFunc(script_path):
    funcList = []
    functions = find_functions_in_script(script_path)
    for func in functions:
        funcList.append(get_function_source(script_path, func))
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

def findIfOrVar(noCommentScriptStr):
    wordScript = noCommentScriptStr.split(" ")
    for i in wordScript:
        if re.search("if|=", i):
            return True
    return False

def findDictionaries(fullScript):
    dictionaries =  "\{(?:[^{}]|(?R))*\})" #gets dictionary literals
    

def findRecursion(fullScript):
    #split into functions, then find function name within the functions
    #def whitespace word (anything ) colon
    funcNames = "def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):" # maps everything from after def to before colon
    funcBlocks = " " # takes the body of the function
    #loop thru funcBlocks to see where funcNames align?

#def findLoops(fullScript):
    #for loop pattern:  for\s+\w+\s+in\s+.+:     (only retrieves the header, not the body of the loop yet)
    # while loop header pattern: while\s+.+:


# def findInheritance(fullScript): 




commentList = []
totalScriptList = []

script_path = "LOC.py"

inputfile = open(script_path, "r")
inputfiletest2 = open(script_path, "r")
noCommentsinputfile = removeComments(inputfiletest2.read())
for x in inputfile:
    totalScriptList.append(x)
    commentList.append(commentCheck(x))
print("The total LOC is: " + str(len(totalScriptList)))


commentList = [z for z in commentList if z != ""]
print("The Cyclomatic Complexity is: " + str(CyclomaticChicanery(noCommentsinputfile)))
  
print("The comment level is: " + str(len(commentList)))
print("The percentage comments is: " + str((len(commentList)/len(totalScriptList))*100))
print("There are " + str(len(funcName(totalScriptList))) + " functions present")
print("These functions are: " + str(funcName(totalScriptList)))
for i in splitFunc(script_path):
    print(i)
#print(splitFunc(script_path))
# print(inspect.getsource(funcName))


#print(find_functions_in_script("LOC.py"))



    
# for i, n in enumerate((splitFunc(totalScriptList))):
#     print(n, i)
#print((splitFunc(totalScriptList)))

# testing on LOC.py
#print(removeComments(inputfiletest2.read()))
#print(inputfiletest2.read())
#print(commentCheck(inputfile.read()))


