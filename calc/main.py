#!/usr/bin/env python3
"""
Command-line calculator with history and result memory
Features:
- Basic arithmetic (+, -, *, /, ^)
- Last result variable (r)
- Command history
- Cross-platform clear screen
"""

import os

class Calculator:
    def __init__(self):
        self.history = []
        self.last_result = None
    
    def run(self):
        """Main REPL loop"""
        print("Calculator (type 'help' for commands)")
        while True:
            try:
                expr = input("> ").strip()
                if not expr:
                    continue
                
                if self._handle_command(expr):
                    continue
                
                result = self._evaluate_expression(expr)
                self.last_result = result
                print(f"= {result}")
                
            except (ValueError, SyntaxError) as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    
    def _handle_command(self, expr):
        """Process non-math commands"""
        cmd = expr.lower()
        if cmd in ('quit', 'q', 'exit'):
            raise KeyboardInterrupt
        elif cmd in ('clear', 'cls', 'c'):
            os.system('cls' if os.name == 'nt' else 'clear')
            return True
        elif cmd == 'history':
            self._show_history()
            return True
        elif cmd == 'help':
            self._show_help()
            return True
        return False

    def _show_help(self):
        """Display available commands"""
        help_text = """
    Calculator Commands:
    +, -, *, /, ^   Basic arithmetic
    ( )             Parentheses for grouping
    r               Use last result (e.g. 'r + 5')
    
    Special Commands:
    help            Show this help
    history         Show calculation history
    clear/cls/c     Clear screen
    quit/q/exit     Exit calculator
    """
        print(help_text.strip())
    
    def _evaluate_expression(self, expr):
        """Core evaluation logic"""
        if 'r' in expr:
            if self.last_result is None:
                raise ValueError("No previous result ('r') available")
            expr = expr.replace('r', str(self.last_result))
        
        tokens = self._tokenize(expr)
        parsed = self._parse(tokens)
        result = self._evaluate(parsed)
        
        self.history.append((expr, result))
        return result

# Lexer
def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)
    
    while i < n:
        if expr[i].isspace():
            i += 1
        elif expr[i] in '()+-*/^':
            tokens.append(expr[i])
            i += 1
        elif expr[i].isdigit() or expr[i] == '.':
            num_str = ''
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                num_str += expr[i]
                i += 1
            if num_str.count('.') > 1:
                raise ValueError("Invalid number format")
            tokens.append(float(num_str) if '.' in num_str else int(num_str))
        else:
            raise ValueError(f"Unknown character: {expr[i]}")
    
    return tokens

# PArser
def parse_expression(tokens):
    output = []
    operators = []
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    for token in tokens:
        if isinstance(token, (int, float)):
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses")
            operators.pop()  
        else: 
            while (operators and operators[-1] != '(' and
                   precedence.get(operators[-1], 0) >= precedence.get(token, 0)):
                output.append(operators.pop())
            operators.append(token)
    
    while operators:
        op = operators.pop()
        if op == '(':
            raise ValueError("Mismatched parentheses")
        output.append(op)
    
    return output

# Evaluator
def evaluate(rpn):
    stack = []
    
    for token in rpn:
        if isinstance(token, (int, float)):
            stack.append(token)
        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Division by zero")
                stack.append(a / b)
            elif token == '^':
                stack.append(a ** b)
    
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    
    return stack[0]

if __name__ == "__main__":
    Calculator().run()
