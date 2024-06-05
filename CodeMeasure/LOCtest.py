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
    


commentList = []
inputfile = open("LOC.txt", "r")
for x in inputfile:
  commentList.append(commentCheck(x))
print("The LOC is: " + str(len(commentList)))
commentList = [z for z in commentList if z != ""]

  
print("The comment level is: " + str(len(commentList)))

#print(commentCheck(inputfile.read()))