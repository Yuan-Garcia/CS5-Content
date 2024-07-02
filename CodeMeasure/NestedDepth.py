import re

class CallChain:
    def __init__(self, functions, funcNames):
        self.functions = functions
        self.names = funcNames
        self.depth = self.findLongestBranch()
        self.totalFuncCalls = 0
        self.maxFunctionCalls = self.findFunctionCalls()

    def findBranches(self, func, funcs, names, currentPath):
        funcBody = func.split(':', 1)[1].strip()  # get everything behind the colon

        funcName = re.search("def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", func).group(1)  # before colon
        print("Function name is\n", funcName)
        print("Function Body is\n", funcBody)
        isRecursive = funcName in funcBody
        # base case: if there is no function call in the function
        if isRecursive or not any(name in funcBody for name in names):  # if function doesn't have another function call or function is recursive, terminate
            print("was recursive? ", isRecursive)
            print('returning path', currentPath)
            return currentPath
        else:
            for name in names:  # if yes, add it to the current path
                if name in funcBody and not isRecursive:
                    newPath = [name]
                    print("MADE IT TO THE ELSE")
                    print('current name in path =', name)
                    nextFunc = funcs[names.index(name)]  # go to function that just got called
                    print(nextFunc)
                    nestedPath = self.findBranches(nextFunc, funcs, names, [])
                    newPath.extend(nestedPath)  # Extend the current path with the nested path
                    currentPath.append(newPath)
            return currentPath
        
    def findLongestBranch(self):  # longest chain of dependencies without recursion, takes in function list and function names list
        allPaths = []
        
        for func in self.functions:
            currentPath = []
            print("\n\n\nCURRENT FUNCTION!!", func)
            currentPath.append(re.search("def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", func).group(1)) 
            path = self.findBranches(func, self.functions, self.names, currentPath)
            print('currentPath appending', path)
            allPaths.append(path)
            print('allPaths =', allPaths)
        
        longestPath = max(allPaths, key=lambda x: self.findMaxDepth(x))
        print('longest chain length is', self.findMaxDepth(longestPath))
        print('Longest chain contains: ', longestPath)
        return self.findMaxDepth(longestPath)

    def findMaxDepth(self, nestedList, currentDepth=0):
        if not isinstance(nestedList, list) or not nestedList:
            return currentDepth
        maxDepth = currentDepth
        for item in nestedList:
            if isinstance(item, list):
                depth = self.findMaxDepth(item, currentDepth + 1)
                maxDepth = max(maxDepth, depth)
        return maxDepth
    
    def findFunctionCalls(self):
        callsList = []
        maxCalls = 0
        for func in self.functions:
            currentNumCalls = 0
            currentPath = []
            print("\n\n\nCURRENT FUNCTION!!", func)
            funcBody = func.split(':', 1)[1].strip()  # get everything behind the colon
            # funcName = re.search("def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", func).group(1)
            for name in self.names:
                if name in funcBody:
                    currentPath.extend(name)
                    self.totalFuncCalls += 1
                    currentNumCalls += 1
            
            maxCalls = max(maxCalls, currentNumCalls)
            callsList.append(currentPath)
            #Note to self, return the LONGEST function calls
        return maxCalls

    # def findFunctionCalls(self):
    #     maxCalls = 0
    #     for func in self.functions:
    #         currentNumCalls = 0
    #         funcBody = func.split(':', 1)[1].strip()  # get everything behind the colon
    #         for name in self.names:
    #             if name in funcBody:
    #                 self.totalFuncCalls += 1
    #                 currentNumCalls += 1
    #         maxCalls = max(maxCalls, currentNumCalls)
    #     return maxCalls