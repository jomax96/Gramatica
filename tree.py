"""
Módulo para representar y visualizar árboles de derivación
"""

from typing import List, Optional


class TreeNode:
    """Nodo de un árbol de derivación"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.children: List['TreeNode'] = []
    
    def add_child(self, child: 'TreeNode'):
        """Añade un hijo al nodo"""
        self.children.append(child)
    
    def is_leaf(self) -> bool:
        """Verifica si el nodo es una hoja"""
        return len(self.children) == 0


class DerivationTree:
    """Árbol de derivación completo"""
    
    def __init__(self, root: TreeNode):
        self.root = root
    
    def to_text(self, node: Optional[TreeNode] = None, prefix: str = "", is_last: bool = True) -> str:
        """
        Convierte el árbol a representación textual con indentación
        
        Args:
            node: Nodo actual (None para comenzar en la raíz)
            prefix: Prefijo de indentación
            is_last: Si este nodo es el último hijo de su padre
        """
        if node is None:
            node = self.root
        
        result = prefix
        if node != self.root:
            result += "└── " if is_last else "├── "
        result += node.symbol + "\n"
        
        if node != self.root:
            prefix += "    " if is_last else "│   "
        
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            result += self.to_text(child, prefix, is_last_child)
        
        return result
    
    def __str__(self):
        """Representación en cadena del árbol"""
        return self.to_text()

