import re 

def commentCheck(comment):
    #hashtags = "[\#[^\n\r]+?(?:[\n\r])]"   # is the actual solution
    hashtags = "[\#]" # is the very temporary solution until I figure out how to get the actual solution to work
    if re.search(hashtags, comment):
        return comment
    else:
        return ""
    #print(commentCheck("#will this work"))
    #print(commentCheck("we will see"))
    
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
            tempFunc = tempFunc + i
        else:
            scriptList.append(tempFunc)
            tempFunc = ""

    return scriptList

commentList = []
totalScriptList = []

inputfile = open("LOC.py", "r")
for x in inputfile:
    totalScriptList.append(x)
    commentList.append(commentCheck(x))
print("The LOC is: " + str(len(totalScriptList)))

commentList = [z for z in commentList if z != ""]

  
print("The comment level is: " + str(len(commentList)))
print("The percentage comments is: " + str((len(commentList)/len(totalScriptList))*100))
#print(splitFunc(totalScriptList))

#print(commentCheck(inputfile.read()))

