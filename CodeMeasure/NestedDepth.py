# import ast

# class AmbitionScoreCalculator:
#     def __init__(self):
#         self.graph = {}

#     def addEdge(self, caller, callee):
#         if caller not in self.graph:
#             self.graph[caller] = []
#         self.graph[caller].append(callee)

#     def dfs(self, node, visited, path, allPaths):
#         visited[node] = True
#         path.append(node)

#         if node not in self.graph or not self.graph[node]:
#             allPaths.append(path.copy())  # Adding path to allPaths
#             print(f"Added path: {path.copy()}")  # Debug print for added paths
#         else:
#             for neighbor in self.graph[node]:
#                 if not visited[neighbor]:
#                     self.dfs(neighbor, visited, path, allPaths)

#         path.pop()
#         visited[node] = False

#     def findLongestBranch(self):
#         allPaths = []
#         visited = {node: False for node in self.graph}

#         for node in self.graph:
#             if not visited[node]:  # Only call dfs if the node is not visited
#                 self.dfs(node, visited, [], allPaths)

#         print("All paths:", allPaths)  # Debug print for allPaths
#         if allPaths:  # Check if allPaths is not empty
#             longestPath = max(allPaths, key=len)
#             return longestPath
#         else:
#             return []

#     def buildFromAST(self, node, currentFunction=None):
#         if isinstance(node, ast.FunctionDef):
#             currentFunction = node.name
#             if currentFunction not in self.graph:
#                 self.graph[currentFunction] = []
#         elif isinstance(node, ast.Call) and currentFunction:
#             if isinstance(node.func, ast.Name):
#                 callee = node.func.id
#                 self.addEdge(currentFunction, callee)
        
#         for child in ast.iter_child_nodes(node):
#             self.buildFromAST(child, currentFunction)

#     def findLongestPath(self, script):
#         tree = ast.parse(script)
#         self.buildFromAST(tree)
#         # print("Graph:", self.graph)  # Debug print for the graph
#         return self.findLongestBranch()