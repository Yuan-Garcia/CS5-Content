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
    addOne = "for|if|for|while|except|with|assert|Comprehension|and|or|not|implies"
    CyclomaticCount = 0
    for i in noCommentScriptStr:
        if re.search(addOne, i):
            CyclomaticCount = CyclomaticCount + 1
    return CyclomaticCount

def removeComments(fullScript):
    multiLine = "\'\'\'[^']*\'\'\'|\"\"\"[^\"]*\"\"\""
    fullScript = re.sub(multiLine, "", fullScript)
    fullScript = re.sub("\#[^\n\r]+?(?:[\n\r])","",fullScript)
    return fullScript



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

def determineFunc(fullScript):
    scriptList = []
    for i,n in enumerate(fullScript):
        if(n.startswith("def ")):
            scriptList.append(i)
    return scriptList

commentList = []
totalScriptList = []

inputfile = open("LOC.py", "r")
inputfiletest2 = open("LOC.py", "r")
for x in inputfile:
    totalScriptList.append(x)
    commentList.append(commentCheck(x))
print("The LOC is: " + str(len(totalScriptList)))

commentList = [z for z in commentList if z != ""]

  
print("The comment level is: " + str(len(commentList)))
print("The percentage comments is: " + str((len(commentList)/len(totalScriptList))*100))
print("There are " + str(len(determineFunc(totalScriptList))) + " functions present")
#print(splitFunc(totalScriptList))

# testing on LOC.py
print(removeComments(inputfiletest2.read()))
#print(inputfiletest2.read())
#print(commentCheck(inputfile.read()))


