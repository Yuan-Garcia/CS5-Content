import re

class StringFormat:
    
    def __init__(self, path):
        self.path = path
        with open(path, "r") as file:
            self.full_script = file.read()
        self.noComments = self.removeComments(self.full_script)
        self.finalString = self.removeTabNewLn(self.noComments)  

    def removeComments(self, fullScript):
        multiLine = "\'\'\'[^']*\'\'\'|\"\"\"[^\"]*\"\"\"" # gets all docstrings
        fullScript = re.sub(multiLine, "", fullScript) # replaces all docstrings with an emptystring
        fullScript = re.sub("#.*","",fullScript) #replaces everything that has a comment with an emptystring
        return fullScript
    
    def removeTabNewLn(self, noCommentsStr):
        noCommentsStr = re.sub("[\t+\n]", "", noCommentsStr)
        # print("the final script is", noCommentsStr)
        return noCommentsStr
    
noStringScript = StringFormat("CodeMeasure/LOC.py")
# print(noStringScript.finalString)
