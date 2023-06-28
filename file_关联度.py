import ast

class CallCollector(ast.NodeVisitor):
    def __init__(self):
        self.calls = set()
        self.imports = set()

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.imports.add(node.module)
        self.generic_visit(node)

def get_calls(filename):
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())
    collector = CallCollector()
    collector.visit(tree)
    return collector.calls

def get_imports(filename):
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())
    collector = CallCollector()
    collector.visit(tree)
    return collector.imports

print(get_imports('git_stats.py'))
print(get_calls('git_stats.py'))    

