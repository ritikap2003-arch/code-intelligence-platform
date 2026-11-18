python -c "
content = '''def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    if b == 0:
        raise ValueError(\"Cannot divide by zero\")
    return a / b

class Calculator:
    def __init__(self):
        self.history = []

    def calculate(self, operation, a, b):
        result = operation(a, b)
        self.history.append(f\"{operation.__name__}({a}, {b}) = {result}\")
        return result

    def get_history(self):
        return self.history
'''
with open('sample_codebase/calculator.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
"