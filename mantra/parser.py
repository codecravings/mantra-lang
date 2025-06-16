from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk
from typing import List, Optional
from .lexer import Token, TokenType
from .ast_nodes import *

class SimpleParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
    
    def match(self, *token_types):
        return self.current_token().type in token_types
    
    def consume(self, token_type):
        if self.current_token().type == token_type:
            token = self.current_token()
            self.advance()
            return token
        raise SyntaxError(f"Expected {token_type}, got {self.current_token().type}")
    
    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse(self):
        statements = []
        self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            if self.match(TokenType.NEWLINE):
                self.advance()
                continue
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return ProgramNode(statements)
    
    def parse_statement(self):
        self.skip_newlines()
        
        if self.match(TokenType.STHANA):
            return self.parse_variable_declaration()
        elif self.match(TokenType.KRIYA):
            return self.parse_function_definition()
        elif self.match(TokenType.YADI):
            return self.parse_if_statement()
        elif self.match(TokenType.PUNAR):
            return self.parse_loop()
        elif self.match(TokenType.GATI):
            return self.parse_return()
        else:
            # Expression or assignment
            expr = self.parse_expression()
            if self.match(TokenType.ASSIGN):
                if isinstance(expr, IdentifierNode):
                    self.advance()
                    value = self.parse_expression()
                    return AssignmentNode(expr.name, value)
            return expr
    
    def parse_variable_declaration(self):
        self.consume(TokenType.STHANA)
        name = self.consume(TokenType.IDENTIFIER).value
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()
            return VariableDeclarationNode(name, value)
        return VariableDeclarationNode(name)
    
    def parse_function_definition(self):
        self.consume(TokenType.KRIYA)
        name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.LPAREN)
        
        params = []
        while not self.match(TokenType.RPAREN):
            params.append(self.consume(TokenType.IDENTIFIER).value)
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE)
        
        body = []
        while not self.match(TokenType.RBRACE):
            self.skip_newlines()
            if self.match(TokenType.RBRACE):
                break
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.consume(TokenType.RBRACE)
        return FunctionDefNode(name, params, body)
    
    def parse_if_statement(self):
        self.consume(TokenType.YADI)
        condition = self.parse_expression()
        self.consume(TokenType.LBRACE)
        
        then_branch = []
        while not self.match(TokenType.RBRACE):
            self.skip_newlines()
            if self.match(TokenType.RBRACE):
                break
            stmt = self.parse_statement()
            if stmt:
                then_branch.append(stmt)
        
        self.consume(TokenType.RBRACE)
        
        else_branch = None
        if self.match(TokenType.ATHAVA):
            self.advance()
            self.consume(TokenType.LBRACE)
            else_branch = []
            while not self.match(TokenType.RBRACE):
                self.skip_newlines()
                if self.match(TokenType.RBRACE):
                    break
                stmt = self.parse_statement()
                if stmt:
                    else_branch.append(stmt)
            self.consume(TokenType.RBRACE)
        
        return IfNode(condition, then_branch, else_branch)
    
    def parse_loop(self):
        self.consume(TokenType.PUNAR)
        condition = self.parse_expression()
        self.consume(TokenType.LBRACE)
        
        body = []
        while not self.match(TokenType.RBRACE):
            self.skip_newlines()
            if self.match(TokenType.RBRACE):
                break
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.consume(TokenType.RBRACE)
        return LoopNode(condition, body)
    
    def parse_return(self):
        self.consume(TokenType.GATI)
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()
        return ReturnNode(value)
    
    def parse_expression(self):
        return self.parse_comparison()
    
    def parse_comparison(self):
        left = self.parse_addition()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS, TokenType.LESS_THAN, 
                         TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.current_token().value
            self.advance()
            right = self.parse_addition()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_addition(self):
        left = self.parse_multiplication()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplication()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_multiplication(self):
        left = self.parse_primary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.current_token().value
            self.advance()
            right = self.parse_primary()
            left = BinaryOpNode(left, op, right)
        
        return left
    
    def parse_primary(self):
        if self.match(TokenType.NUMBER):
            value = float(self.current_token().value)
            self.advance()
            return NumberNode(value)
        
        if self.match(TokenType.STRING):
            value = self.current_token().value
            self.advance()
            return StringNode(value)
        
        if self.match(TokenType.SATY):
            self.advance()
            return BooleanNode(True)
        
        if self.match(TokenType.ASATY):
            self.advance()
            return BooleanNode(False)
        
        if self.match(TokenType.SHUNYA):
            self.advance()
            return NullNode()
        
        if self.match(TokenType.IDENTIFIER):
            name = self.current_token().value
            self.advance()
            
            # Function call
            if self.match(TokenType.LPAREN):
                self.advance()
                args = []
                while not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    if self.match(TokenType.COMMA):
                        self.advance()
                self.consume(TokenType.RPAREN)
                return FunctionCallNode(name, args)
            
            return IdentifierNode(name)
        
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        
        raise SyntaxError(f"Unexpected token: {self.current_token().type}")
