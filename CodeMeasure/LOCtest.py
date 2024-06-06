import re 

def commentCheck(comment):
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
    addOne = "for|if|for|while|except|with|assert|Comprehension|and|or|not|implies"
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

def funcName(fullScript):
    tempList = []
    ansList = []
    getNames = "(def [a-zA-Z_]+( [^(]+)*)" #gets only the def (name)
    for i in fullScript:
        if re.search(getNames, i):
            tempList.append(i)
    for n, i in enumerate(tempList):
        ansList.append((i.split("(")[0])[4:]) #parses out the variable and the "def ", giving only the variable name
    return ansList

def splitFunc(fullScript):
    scriptList = []
    tempFunc = ""
    funcToggle = False
    for i in fullScript:
        if(i.startswith("def ")):
            funcToggle = True
        elif((i.startswith(" ") or i.startswith("\t"))):# or i.startswith("#"))):
            funcToggle = True
        else:
            funcToggle = False
        if funcToggle:
            tempFunc = tempFunc + i #the reason that this method sucks is that if people make a return line with no spaces then it calls it a new function, which no PERSON does, but LLM's do
        else:
            scriptList.append(tempFunc)
            tempFunc = ""

    return scriptList

commentList = []
totalScriptList = []

inputfile = open("LOC.py", "r")
inputfiletest2 = open("LOC.py", "r")
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
#print(splitFunc(totalScriptList))

# testing on LOC.py
#print(removeComments(inputfiletest2.read()))
#print(inputfiletest2.read())
#print(commentCheck(inputfile.read()))


