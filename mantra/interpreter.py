import re
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Dict, Any
from .ast_nodes import *


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
        self.functions = {}
    
    def define(self, name, value):
        self.variables[name] = value
    
    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        return None
    
    def set(self, name, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent and name in self.parent.variables:
            self.parent.set(name, value)
        else:
            self.variables[name] = value
    
    def define_function(self, name, func):
        self.functions[name] = func
    
    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        return None

class MantraFunction:
    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class SimpleInterpreter:
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.setup_builtins()
    
    def setup_builtins(self):
        # Sanskrit built-in functions
        def prakash(*args):
            print(*args)
            return None
        
        def lambh(obj):
            if obj is None:
                return 0
            try:
                return len(str(obj))
            except:
                return 0
        
        def shabd(obj):
            return str(obj) if obj is not None else "shunya"
        
        def ank(obj):
            try:
                return int(float(obj)) if obj is not None else 0
            except:
                return 0
        
        # Register functions
        self.global_env.define_function('prakash', prakash)
        self.global_env.define_function('lambh', lambh)
        self.global_env.define_function('shabd', shabd)
        self.global_env.define_function('ank', ank)
        
        # English aliases
        self.global_env.define_function('print', prakash)
        self.global_env.define_function('len', lambh)
        self.global_env.define_function('str', shabd)
        self.global_env.define_function('int', ank)
    
    def interpret(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, None)
        if method:
            return method(node)
        return None
    
    def visit_ProgramNode(self, node):
        result = None
        for statement in node.statements:
            try:
                result = self.interpret(statement)
            except ReturnValue as ret:
                return ret.value
        return result
    
    def visit_NumberNode(self, node):
        return node.value
    
    def visit_StringNode(self, node):
        return node.value
    
    def visit_BooleanNode(self, node):
        return node.value
    
    def visit_NullNode(self, node):
        return None
    
    def visit_IdentifierNode(self, node):
        return self.current_env.get(node.name)
    
    def visit_BinaryOpNode(self, node):
        left = self.interpret(node.left)
        right = self.interpret(node.right)
        
        # Handle None values
        if left is None:
            left = 0
        if right is None:
            right = 0
        
        try:
            if node.operator == '+':
                return left + right
            elif node.operator == '-':
                return left - right
            elif node.operator == '*':
                return left * right
            elif node.operator == '/':
                return left / right if right != 0 else 0
            elif node.operator == '==':
                return left == right
            elif node.operator == '!=':
                return left != right
            elif node.operator == '<':
                return left < right
            elif node.operator == '>':
                return left > right
            elif node.operator == '<=':
                return left <= right
            elif node.operator == '>=':
                return left >= right
        except:
            return 0
    
    def visit_AssignmentNode(self, node):
        value = self.interpret(node.value)
        self.current_env.set(node.name, value)
        return value
    
    def visit_VariableDeclarationNode(self, node):
        value = None
        if node.value:
            value = self.interpret(node.value)
        self.current_env.define(node.name, value)
        return value
    
    def visit_FunctionDefNode(self, node):
        func = MantraFunction(node.name, node.params, node.body, self.current_env)
        self.current_env.define_function(node.name, func)
        return func
    
    def visit_FunctionCallNode(self, node):
        func = self.current_env.get_function(node.name)
        if not func:
            return None
        
        args = [self.interpret(arg) for arg in node.args]
        
        # Built-in function
        if callable(func):
            try:
                return func(*args)
            except:
                return None
        
        # User-defined function
        if isinstance(func, MantraFunction):
            if len(args) != len(func.params):
                return None
            
            # Create new environment
            func_env = Environment(func.closure)
            for param, arg in zip(func.params, args):
                func_env.define(param, arg)
            
            # Execute function
            prev_env = self.current_env
            self.current_env = func_env
            
            try:
                result = None
                for statement in func.body:
                    result = self.interpret(statement)
                return result
            except ReturnValue as ret:
                return ret.value
            finally:
                self.current_env = prev_env
        
        return None
    
    def visit_IfNode(self, node):
        condition = self.interpret(node.condition)
        
        if condition:
            result = None
            for stmt in node.then_branch:
                result = self.interpret(stmt)
            return result
        elif node.else_branch:
            result = None
            for stmt in node.else_branch:
                result = self.interpret(stmt)
            return result
        return None
    
    def visit_LoopNode(self, node):
        result = None
        count = 0
        max_iterations = 1000  # Prevent infinite loops
        
        while count < max_iterations:
            condition = self.interpret(node.condition)
            if not condition:
                break
            
            for stmt in node.body:
                result = self.interpret(stmt)
            count += 1
        
        return result
    
    def visit_ReturnNode(self, node):
        value = None
        if node.value:
            value = self.interpret(node.value)
        raise ReturnValue(value)