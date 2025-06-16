"""
Mantra Programming Language
A Sanskrit-inspired language for concise, expressive programming
"""

__version__ = "0.1.0"
__author__ = "Mantra Team"

from .lexer import SimpleLexer as Lexer
from .parser import SimpleParser as Parser  
from .interpreter import SimpleInterpreter as Interpreter

class MantraRunner:
    def __init__(self):
        self.interpreter = Interpreter()
    
    def run_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.run_code(code)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def run_code(self, code):
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            result = self.interpreter.interpret(ast)
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def repl(self):
        print("Mantra Programming Language REPL v0.1.0")
        print("Type 'exit' to quit")
        print("॥ Om Gam Ganapataye Namaha ॥")
        print()
        
        while True:
            try:
                code = input("mantra> ")
                if code.lower() in ['exit', 'quit']:
                    break
                
                if code.strip():
                    result = self.run_code(code)
                    if result is not None:
                        print(result)
                        
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                break