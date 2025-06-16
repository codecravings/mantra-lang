from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk
from typing import List, Optional
from .lexer import Token, TokenType


class ASTNode:
    pass

@dataclass
class NumberNode(ASTNode):
    value: float

@dataclass
class StringNode(ASTNode):
    value: str

@dataclass
class BooleanNode(ASTNode):
    value: bool

@dataclass
class NullNode(ASTNode):
    pass

@dataclass
class IdentifierNode(ASTNode):
    name: str

@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class AssignmentNode(ASTNode):
    name: str
    value: ASTNode

@dataclass
class VariableDeclarationNode(ASTNode):
    name: str
    value: Optional[ASTNode] = None

@dataclass
class FunctionDefNode(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode]

@dataclass
class FunctionCallNode(ASTNode):
    name: str
    args: List[ASTNode]

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None

@dataclass
class LoopNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]