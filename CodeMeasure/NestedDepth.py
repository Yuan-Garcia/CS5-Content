# import ast

# class FunctionCallVisitor(ast.NodeVisitor):
#     def __init__(self):
#         self.functions = {}
#         self.current_function = None

#     def visit_FunctionDef(self, node):
#         self.current_function = node.name
#         self.functions[node.name] = []
#         self.generic_visit(node)

#     def visit_Call(self, node):
#         if self.current_function is not None:
#             if isinstance(node.func, ast.Name):
#                 self.functions[self.current_function].append(node.func.id)
#         self.generic_visit(node)

# def build_call_graph(script_path):
#     with open(script_path, "r") as file:
#         tree = ast.parse(file.read(), filename=script_path)
    
#     visitor = FunctionCallVisitor()
#     visitor.visit(tree)
#     return visitor.functions

# def measure_ambition(call_graph):
#     def visit(function, visited):
#         if function in visited:
#             return 0
#         visited.add(function)
#         max_depth = 0
#         for callee in call_graph.get(function, []):
#             max_depth = max(max_depth, visit(callee, visited))
#         visited.remove(function)
#         return max_depth + 1

#     max_chain_length = 0
#     for function in call_graph:
#         max_chain_length = max(max_chain_length, visit(function, set()))
#     return max_chain_length

# # # Example usage
# # script_path = "LOC.py"
# # call_graph = build_call_graph(script_path)
# # ambition_score = measure_ambition(call_graph)

# # print(f"Ambition score (max chain length): {ambition_score}")
import ast

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = {}
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.functions[node.name] = []
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function is not None:
            if isinstance(node.func, ast.Name):
                self.functions[self.current_function].append(node.func.id)
        self.generic_visit(node)

def build_call_graph(script_path):
    with open(script_path, "r") as file:
        tree = ast.parse(file.read(), filename=script_path)
    
    visitor = FunctionCallVisitor()
    visitor.visit(tree)
    return visitor.functions

def measure_ambition(call_graph):
    def visit(function, visited):
        if function in visited:
            return 0
        visited.add(function)
        max_depth = 0
        for callee in call_graph.get(function, []):
            if callee in call_graph:
                max_depth = max(max_depth, visit(callee, visited))
        visited.remove(function)
        return max_depth + 1

    max_chain_length = 0
    for function in call_graph:
        max_chain_length = max(max_chain_length, visit(function, set()))
    return max_chain_length

# Example usage
# script_path = "LOC.py"
# call_graph = build_call_graph(script_path)
# ambition_score = measure_ambition(call_graph)

# print(f"Ambition score (max chain length): {ambition_score}")
