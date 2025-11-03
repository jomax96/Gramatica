"""
Módulo para generar cadenas del lenguaje usando BFS
"""

from typing import List, Set, Tuple, Deque
from collections import deque
from grammar import Grammar


class StringGenerator:
    """Generador de cadenas para gramáticas"""
    
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
    
    def generate_strings(self, max_count: int = 10) -> List[str]:
        """
        Genera las primeras max_count cadenas más cortas usando BFS
        
        Args:
            max_count: Número máximo de cadenas a generar
            
        Returns:
            Lista de cadenas ordenadas por longitud
        """
        generated: List[str] = []
        visited: Set[str] = set()  # Para evitar duplicados
        
        # Cola para BFS: (cadena_actual, profundidad)
        queue: Deque[Tuple[str, int]] = deque()
        queue.append((self.grammar.start_symbol, 0))
        visited.add(self.grammar.start_symbol)
        
        max_depth = 20  # Límite de profundidad para evitar bucles infinitos
        
        while queue and len(generated) < max_count:
            current, depth = queue.popleft()
            
            if depth > max_depth:
                continue
            
            # Verificar si es una cadena terminal (solo contiene terminales)
            if self._is_terminal_string(current):
                # Limpiar símbolos no terminales residuales (no debería pasar)
                clean_string = self._clean_string(current)
                if clean_string not in generated:
                    generated.append(clean_string)
                continue
            
            # Aplicar todas las producciones posibles
            for i in range(len(current)):
                symbol = current[i]
                if symbol in self.grammar.non_terminals:
                    # Reemplazar este símbolo con todas sus producciones
                    for production in self.grammar.productions.get(symbol, []):
                        new_string = current[:i] + production + current[i+1:]
                        
                        # Evitar duplicados
                        if new_string not in visited:
                            visited.add(new_string)
                            queue.append((new_string, depth + 1))
                    break  # Solo reemplazar el primer no terminal encontrado (BFS por niveles)
        
        return generated[:max_count]
    
    def _is_terminal_string(self, string: str) -> bool:
        """Verifica si una cadena contiene solo símbolos terminales"""
        for char in string:
            if char in self.grammar.non_terminals:
                return False
        return True
    
    def _clean_string(self, string: str) -> str:
        """Limpia una cadena eliminando espacios y caracteres especiales"""
        return string.replace('ε', '').replace(' ', '')

