"""
Módulo para parsing de gramáticas (Tipo 2 y Tipo 3)
"""

from typing import List, Optional, Tuple, Set
from grammar import Grammar
from tree import DerivationTree, TreeNode


class Parser:
    """Clase base para parsers"""
    
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
    
    def parse(self, string: str) -> Tuple[bool, Optional[DerivationTree]]:
        """
        Analiza si una cadena pertenece al lenguaje
        
        Returns:
            (aceptada, árbol_de_derivación)
        """
        raise NotImplementedError


class Type3Parser(Parser):
    """Parser para gramáticas Tipo 3 (Regulares) usando autómata finito"""
    
    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
        # Preprocesar terminales ordenados por longitud (más largos primero)
        self._sorted_terminals = sorted(self.grammar.terminals, key=len, reverse=True)
        self.automaton = self._build_automaton()
    
    def _build_automaton(self) -> dict:
        """
        Construye un autómata finito no determinista desde la gramática regular
        Returns: dict con estados y transiciones
        """
        # Estados: no terminales + estado final
        states = set(self.grammar.non_terminals)
        states.add('FINAL')  # Estado de aceptación
        
        transitions = {}  # {estado: {símbolo: [estados_destino]}}
        
        # Inicializar transiciones
        for state in states:
            transitions[state] = {}
        
        # Construir transiciones desde las producciones
        for left, rights in self.grammar.productions.items():
            for right in rights:
                # Para gramáticas regulares, las producciones pueden ser:
                # A → a (terminal simple)
                # A → aB (terminal seguido de no terminal)
                # A → ε (cadena vacía)
                
                if right == '' or right == 'ε':
                    # Producción vacía - transición directa al final
                    if 'ε' not in transitions[left]:
                        transitions[left]['ε'] = []
                    transitions[left]['ε'].append('FINAL')
                elif right in self.grammar.terminals:
                    # A → a (solo terminal)
                    terminal = right
                    if terminal not in transitions[left]:
                        transitions[left][terminal] = []
                    transitions[left][terminal].append('FINAL')
                else:
                    # Intentar parsear A → aB o A → terminal_multi_carácter
                    # Buscar el terminal más largo al inicio
                    matched_terminal = None
                    remaining = right
                    
                    # Buscar terminal en el inicio
                    for terminal in self._sorted_terminals:
                        if remaining.startswith(terminal):
                            matched_terminal = terminal
                            remaining = remaining[len(terminal):]
                            break
                    
                    if matched_terminal:
                        if len(remaining) == 0:
                            # A → terminal (lleva al final)
                            if matched_terminal not in transitions[left]:
                                transitions[left][matched_terminal] = []
                            transitions[left][matched_terminal].append('FINAL')
                        elif len(remaining) == 1 and remaining in self.grammar.non_terminals:
                            # A → terminal B
                            if matched_terminal not in transitions[left]:
                                transitions[left][matched_terminal] = []
                            transitions[left][matched_terminal].append(remaining)
        
        return {
            'states': states,
            'transitions': transitions,
            'initial': self.grammar.start_symbol,
            'final': 'FINAL'
        }
    
    def _try_match_terminal(self, string: str, pos: int) -> Optional[Tuple[int, str]]:
        """
        Intenta hacer match de un terminal en la posición dada
        Prueba terminales más largos primero para evitar conflictos
        """
        remaining = string[pos:]
        
        # Intentar con terminales más largos primero
        for terminal in self._sorted_terminals:
            if remaining.startswith(terminal):
                return (pos + len(terminal), terminal)
        
        return None
    
    def parse(self, string: str) -> Tuple[bool, Optional[DerivationTree]]:
        """Analiza una cadena usando el autómata finito"""
        if not string:  # Cadena vacía
            # Verificar si hay producción vacía
            if '' in self.grammar.productions.get(self.grammar.start_symbol, []) or \
               'ε' in self.grammar.productions.get(self.grammar.start_symbol, []):
                root = TreeNode(self.grammar.start_symbol)
                root.add_child(TreeNode('ε'))
                return True, DerivationTree(root)
            return False, None
        
        # Simular autómata finito no determinista con terminales multi-carácter
        current_states = {self.grammar.start_symbol}
        
        # Guardar rastro para construir el árbol
        trace = []  # Lista de (estado, terminal_matcheado, estados_siguientes)
        
        pos = 0
        while pos < len(string):
            next_states = set()
            used_transitions = []
            matched_terminal = None
            
            # Intentar hacer match con terminales (más largos primero)
            match_result = self._try_match_terminal(string, pos)
            
            if match_result is None:
                # No hay match posible
                return False, None
            
            new_pos, matched_terminal = match_result
            
            # Procesar transiciones con este terminal
            for state in current_states:
                if matched_terminal in self.automaton['transitions'].get(state, {}):
                    for next_state in self.automaton['transitions'][state][matched_terminal]:
                        next_states.add(next_state)
                        used_transitions.append((state, matched_terminal, next_state))
            
            if not next_states:
                return False, None
            
            trace.append((current_states, matched_terminal, used_transitions))
            current_states = next_states
            pos = new_pos
        
        # Verificar si llegamos al estado final
        if self.automaton['final'] in current_states:
            tree = self._build_tree_from_trace(string, trace)
            return True, tree
        
        return False, None
    
    def _build_tree_from_trace(self, string: str, trace: List) -> DerivationTree:
        """Construye el árbol de derivación desde el rastro"""
        # Implementación simplificada para Tipo 3
        # En gramáticas regulares, el árbol es más lineal
        root = TreeNode(self.grammar.start_symbol)
        current = root
        
        for i, (states, matched_terminal, transitions) in enumerate(trace):
            if transitions:
                state, terminal, next_state = transitions[0]
                child = TreeNode(terminal)
                current.add_child(child)
                if i < len(trace) - 1:
                    current = child
        
        return DerivationTree(root)


class Type2Parser(Parser):
    """Parser para gramáticas Tipo 2 (Libres de Contexto) usando algoritmo recursivo descendente"""
    
    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
        # Preprocesar terminales ordenados por longitud (más largos primero) para matching correcto
        self._sorted_terminals = sorted(self.grammar.terminals, key=len, reverse=True)
    
    def parse(self, string: str) -> Tuple[bool, Optional[DerivationTree]]:
        """
        Analiza una cadena usando parsing recursivo descendente con backtracking
        """
        if not string:  # Cadena vacía
            if '' in self.grammar.productions.get(self.grammar.start_symbol, []) or \
               'ε' in self.grammar.productions.get(self.grammar.start_symbol, []):
                root = TreeNode(self.grammar.start_symbol)
                root.add_child(TreeNode('ε'))
                return True, DerivationTree(root)
            return False, None
        
        # Intentar parsear con backtracking
        result = self._parse_recursive(string, 0, self.grammar.start_symbol, [], 0)
        
        if result and result[0] == len(string):
            tree = result[1]
            return True, tree
        else:
            return False, None
    
    def _try_match_terminal(self, string: str, pos: int) -> Optional[Tuple[int, str]]:
        """
        Intenta hacer match de un terminal en la posición dada
        Prueba terminales más largos primero para evitar conflictos
        
        Returns:
            None si no hay match, (nueva_posición, terminal_matcheado) si hay match
        """
        remaining = string[pos:]
        
        # Intentar con terminales más largos primero
        for terminal in self._sorted_terminals:
            if remaining.startswith(terminal):
                return (pos + len(terminal), terminal)
        
        return None
    
    def _parse_recursive(self, string: str, pos: int, symbol: str, used_productions: List, depth: int = 0) -> Optional[Tuple[int, DerivationTree]]:
        """
        Parsing recursivo con backtracking
        
        Args:
            depth: Profundidad de recursión para evitar bucles infinitos
        
        Returns:
            None si falla, (nueva_posición, árbol) si tiene éxito
        """
        # Protección contra recursión infinita
        if depth > len(string) * 2:
            return None
        
        node = TreeNode(symbol)
        
        # PRIORIDAD: Si el símbolo es no terminal Y está en producciones, tratarlo como no terminal
        # Esto resuelve el conflicto cuando un símbolo está en ambos conjuntos
        if symbol in self.grammar.productions:
            # Es un no terminal, probar todas sus producciones
            # IMPORTANTE: Probar todas las producciones y elegir la que consume más caracteres
            best_result = None
            best_pos = pos
            
            for production in self.grammar.productions[symbol]:
                # Probar esta producción
                current_pos = pos
                production_node = TreeNode(symbol)
                success = True
                
                # Parsear cada símbolo de la producción
                # Primero intentar split por espacios, si no funciona, intentar identificar símbolos
                prod_symbols = self._parse_production_symbols(production)
                
                for prod_sym in prod_symbols:
                    # Manejar cadena vacía
                    if prod_sym == 'ε' or prod_sym == '':
                        production_node.add_child(TreeNode('ε'))
                        continue
                    
                    # Intentar parsear este símbolo
                    result = self._parse_recursive(string, current_pos, prod_sym, used_productions + [(symbol, production)], depth + 1)
                    
                    if result is None:
                        success = False
                        break
                    
                    new_pos, child_tree = result
                    # Verificar que no retrocedimos
                    if new_pos < current_pos:
                        # Si retrocedimos, algo está mal
                        success = False
                        break
                    
                    # Si no avanzamos, puede ser válido si el símbolo puede generar ε
                    # (esto se maneja naturalmente si new_pos == current_pos y el símbolo puede ser vacío)
                    current_pos = new_pos
                    production_node.add_child(child_tree.root)
                
                # Si esta producción funcionó, guardarla si es mejor o igual que las anteriores
                if success:
                    if current_pos > best_pos:
                        # Esta producción consume más caracteres, es mejor
                        best_result = (current_pos, DerivationTree(production_node))
                        best_pos = current_pos
                    elif current_pos == best_pos and best_result is None:
                        # Primera producción exitosa con esta posición
                        best_result = (current_pos, DerivationTree(production_node))
                    # Si la producción es solo ε y estamos en el final, también considerar
                    elif current_pos == pos and ('ε' in prod_symbols or '' in prod_symbols):
                        if best_result is None:
                            best_result = (current_pos, DerivationTree(production_node))
            
            # Retornar el mejor resultado encontrado
            if best_result:
                return best_result
        
        # Si el símbolo es terminal (y NO es no terminal), intentar hacer match
        if symbol in self.grammar.terminals:
            match_result = self._try_match_terminal(string, pos)
            if match_result:
                new_pos, matched_terminal = match_result
                # Verificar que el terminal matcheado sea exactamente el símbolo buscado
                if matched_terminal == symbol:
                    node.add_child(TreeNode(symbol))
                    return (new_pos, DerivationTree(node))
            return None
        
        return None
    
    def _parse_production_symbols(self, production: str) -> List[str]:
        """
        Parsea los símbolos de una producción, reconociendo terminales multi-carácter
        Prioriza no terminales cuando hay ambigüedad
        """
        if not production.strip():
            return []
        
        # Si la producción contiene espacios, split por espacios
        if ' ' in production:
            return [s.strip() for s in production.split() if s.strip()]
        
        # Si no hay espacios, intentar identificar símbolos
        # Esto es más complejo: necesitamos distinguir entre caracteres individuales
        # y terminales multi-carácter, y también reconocer no terminales con apóstrofes como "S'"
        symbols = []
        i = 0
        while i < len(production):
            char = production[i]
            remaining = production[i:]
            matched = False
            
            # PRIMERO: Verificar si hay un no terminal que empiece aquí (incluyendo apóstrofes)
            # Buscar no terminales de mayor longitud primero (para capturar "S'" antes que "S")
            for nt in sorted(self.grammar.non_terminals, key=len, reverse=True):
                if remaining.startswith(nt):
                    symbols.append(nt)
                    i += len(nt)
                    matched = True
                    break
            
            if matched:
                continue
            
            # Si no es no terminal, buscar terminales multi-carácter
            for terminal in sorted(self.grammar.terminals, key=len, reverse=True):
                if remaining.startswith(terminal):
                    symbols.append(terminal)
                    i += len(terminal)
                    matched = True
                    break
            
            # Si no encontramos nada, tratar como carácter individual
            if not matched:
                symbols.append(char)
                i += 1
        
        return symbols
    


def create_parser(grammar: Grammar) -> Parser:
    """Factory para crear el parser apropiado según el tipo de gramática"""
    if grammar.type == "Tipo 3":
        return Type3Parser(grammar)
    else:
        return Type2Parser(grammar)

