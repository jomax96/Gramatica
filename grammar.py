"""
Módulo para representar y trabajar con gramáticas formales (Tipo 2 y Tipo 3)
"""

from typing import Set, List, Dict, Tuple, Optional
from collections import deque
import json


class Grammar:
    """Clase para representar una gramática formal G = (N, T, P, S)"""
    
    def __init__(self, name: str = "", grammar_type: str = "Tipo 2"):
        """
        Inicializa una gramática
        
        Args:
            name: Nombre de la gramática
            grammar_type: "Tipo 2" (Libre de Contexto) o "Tipo 3" (Regular)
        """
        self.name = name
        self.type = grammar_type  # "Tipo 2" o "Tipo 3"
        self.non_terminals: Set[str] = set()  # N
        self.terminals: Set[str] = set()  # T
        self.productions: Dict[str, List[str]] = {}  # P: {no_terminal: [producciones]}
        self.start_symbol: Optional[str] = None  # S
    
    def add_non_terminal(self, symbol: str):
        """Añade un símbolo no terminal"""
        self.non_terminals.add(symbol)
        if symbol not in self.productions:
            self.productions[symbol] = []
    
    def add_terminal(self, symbol: str):
        """Añade un símbolo terminal"""
        self.terminals.add(symbol)
    
    def add_production(self, left: str, right: str):
        """
        Añade una producción left → right
        
        Args:
            left: Lado izquierdo de la producción (debe ser no terminal)
            right: Lado derecho de la producción
        """
        if left not in self.non_terminals:
            self.add_non_terminal(left)
        self.productions[left].append(right)
    
    def set_start_symbol(self, symbol: str):
        """Establece el símbolo inicial"""
        if symbol not in self.non_terminals:
            self.add_non_terminal(symbol)
        self.start_symbol = symbol
    
    def validate(self) -> Tuple[bool, str]:
        """
        Valida que la gramática esté bien formada
        
        Returns:
            (es_válida, mensaje_error)
        """
        if not self.start_symbol:
            return False, "No se ha definido el símbolo inicial"
        
        if self.start_symbol not in self.non_terminals:
            return False, f"El símbolo inicial '{self.start_symbol}' no está en los no terminales"
        
        if len(self.non_terminals) == 0:
            return False, "No hay símbolos no terminales definidos"
        
        if len(self.terminals) == 0:
            return False, "No hay símbolos terminales definidos"
        
        if len(self.productions) == 0:
            return False, "No hay producciones definidas"
        
        # Verificar que todas las producciones tengan su lado izquierdo en N
        for left in self.productions:
            if left not in self.non_terminals:
                return False, f"La producción con lado izquierdo '{left}' no está en los no terminales"
        
        # Validar tipo de gramática
        if self.type == "Tipo 3":
            for left, rights in self.productions.items():
                for right in rights:
                    # Tipo 3: A → aB o A → a (forma normal derecha) o A → Ba o A → a (forma normal izquierda)
                    # Para simplificar, validamos que tenga máximo un no terminal y que esté al final o inicio
                    non_term_count = sum(1 for char in right if char in self.non_terminals)
                    if non_term_count > 1:
                        return False, f"Gramática Tipo 3: la producción {left} → {right} tiene más de un no terminal"
        
        return True, "Gramática válida"
    
    def to_dict(self) -> dict:
        """Convierte la gramática a un diccionario para serialización"""
        return {
            "name": self.name,
            "type": self.type,
            "non_terminals": list(self.non_terminals),
            "terminals": list(self.terminals),
            "productions": self.productions,
            "start_symbol": self.start_symbol
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Grammar':
        """Crea una gramática desde un diccionario"""
        grammar = cls(data.get("name", ""), data.get("type", "Tipo 2"))
        grammar.non_terminals = set(data.get("non_terminals", []))
        grammar.terminals = set(data.get("terminals", []))
        grammar.productions = data.get("productions", {})
        grammar.start_symbol = data.get("start_symbol")
        return grammar
    
    def save_to_file(self, filename: str):
        """Guarda la gramática en un archivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Grammar':
        """Carga una gramática desde un archivo JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def __str__(self):
        """Representación en cadena de la gramática"""
        result = f"Gramática: {self.name}\n"
        result += f"Tipo: {self.type}\n"
        result += f"N (No Terminales): {', '.join(sorted(self.non_terminals))}\n"
        result += f"T (Terminales): {', '.join(sorted(self.terminals))}\n"
        result += f"S (Símbolo Inicial): {self.start_symbol}\n"
        result += "P (Producciones):\n"
        for left in sorted(self.productions.keys()):
            for right in self.productions[left]:
                result += f"  {left} → {right}\n"
        return result

