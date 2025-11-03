"""
Interfaz gráfica de usuario para el Analizador Sintáctico
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from grammar import Grammar
from parser import create_parser
from generator import StringGenerator
import json


class GrammarApp:
    """Aplicación principal con interfaz gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico y Generador de Lenguajes")
        self.root.geometry("1000x700")
        
        self.current_grammar: Grammar = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña 1: Definición de Gramática
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Definir Gramática")
        self._create_grammar_tab(tab1)
        
        # Pestaña 2: Parsing
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Analizar Cadena")
        self._create_parse_tab(tab2)
        
        # Pestaña 3: Generar Cadenas
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Generar Cadenas")
        self._create_generate_tab(tab3)
        
        # Pestaña 4: Visualizar Gramática
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="Ver Gramática")
        self._create_view_tab(tab4)
    
    def _create_grammar_tab(self, parent):
        """Crea la pestaña de definición de gramática"""
        # Frame principal con scroll
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Nombre y tipo
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_frame, text="Nombre:").pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(name_frame, text="Tipo:").pack(side=tk.LEFT, padx=5)
        self.type_var = tk.StringVar(value="Tipo 2")
        type_combo = ttk.Combobox(name_frame, textvariable=self.type_var, 
                                  values=["Tipo 2", "Tipo 3"], state="readonly", width=10)
        type_combo.pack(side=tk.LEFT, padx=5)
        
        # Símbolo inicial
        start_frame = ttk.Frame(main_frame)
        start_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(start_frame, text="Símbolo Inicial (S):").pack(side=tk.LEFT, padx=5)
        self.start_entry = ttk.Entry(start_frame, width=10)
        self.start_entry.pack(side=tk.LEFT, padx=5)
        
        # No terminales
        nt_frame = ttk.LabelFrame(main_frame, text="No Terminales (N)")
        nt_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        nt_input_frame = ttk.Frame(nt_frame)
        nt_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(nt_input_frame, text="Símbolo:").pack(side=tk.LEFT, padx=5)
        self.nt_entry = ttk.Entry(nt_input_frame, width=10)
        self.nt_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(nt_input_frame, text="Añadir", command=self._add_non_terminal).pack(side=tk.LEFT, padx=5)
        
        self.nt_listbox = tk.Listbox(nt_frame, height=5)
        self.nt_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        nt_button_frame = ttk.Frame(nt_frame)
        nt_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(nt_button_frame, text="Eliminar Seleccionado", command=self._remove_non_terminal).pack(side=tk.LEFT, padx=5)
        
        # Terminales
        t_frame = ttk.LabelFrame(main_frame, text="Terminales (T) - Pueden incluir espacios y múltiples caracteres")
        t_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        t_input_frame = ttk.Frame(t_frame)
        t_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(t_input_frame, text="Símbolo:").pack(side=tk.LEFT, padx=5)
        self.t_entry = ttk.Entry(t_input_frame, width=30)
        self.t_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(t_input_frame, text="Añadir", command=self._add_terminal).pack(side=tk.LEFT, padx=5)
        
        self.t_listbox = tk.Listbox(t_frame, height=5)
        self.t_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        t_button_frame = ttk.Frame(t_frame)
        t_button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(t_button_frame, text="Eliminar Seleccionado", command=self._remove_terminal).pack(side=tk.LEFT, padx=5)
        
        # Producciones
        p_frame = ttk.LabelFrame(main_frame, text="Producciones (P)")
        p_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        p_input_frame = ttk.Frame(p_frame)
        p_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(p_input_frame, text="Izquierdo:").pack(side=tk.LEFT, padx=5)
        self.p_left_entry = ttk.Entry(p_input_frame, width=10)
        self.p_left_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(p_input_frame, text="→ Derecho:").pack(side=tk.LEFT, padx=5)
        self.p_right_entry = ttk.Entry(p_input_frame, width=20)
        self.p_right_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(p_input_frame, text="Añadir", command=self._add_production).pack(side=tk.LEFT, padx=5)
        
        self.p_listbox = tk.Listbox(p_frame, height=8)
        self.p_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Nueva Gramática", command=self._new_grammar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Validar", command=self._validate_grammar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Guardar", command=self._save_grammar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cargar", command=self._load_grammar).pack(side=tk.LEFT, padx=5)
    
    def _create_parse_tab(self, parent):
        """Crea la pestaña de parsing"""
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Entrada de cadena
        input_frame = ttk.LabelFrame(main_frame, text="Cadena a Analizar")
        input_frame.pack(fill=tk.X, pady=5)
        
        string_frame = ttk.Frame(input_frame)
        string_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(string_frame, text="Cadena:").pack(side=tk.LEFT, padx=5)
        self.parse_entry = ttk.Entry(string_frame, width=40)
        self.parse_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(string_frame, text="Analizar", command=self._parse_string).pack(side=tk.LEFT, padx=5)
        
        # Resultado
        result_frame = ttk.LabelFrame(main_frame, text="Resultado")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_label = ttk.Label(result_frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)
        
        # Árbol de derivación
        tree_frame = ttk.LabelFrame(main_frame, text="Árbol de Derivación")
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.tree_text = scrolledtext.ScrolledText(tree_frame, height=15, font=("Consolas", 10))
        self.tree_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _create_generate_tab(self, parent):
        """Crea la pestaña de generación de cadenas"""
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botón de generar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Generar 10 Cadenas Más Cortas", 
                   command=self._generate_strings).pack(padx=5)
        
        # Lista de cadenas generadas
        list_frame = ttk.LabelFrame(main_frame, text="Cadenas Generadas")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.strings_listbox = tk.Listbox(list_frame, font=("Consolas", 10))
        self.strings_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _create_view_tab(self, parent):
        """Crea la pestaña de visualización de gramática"""
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.view_text = scrolledtext.ScrolledText(main_frame, font=("Consolas", 10))
        self.view_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Button(main_frame, text="Actualizar Vista", 
                   command=self._update_view).pack(pady=5)
    
    # Métodos de eventos
    def _add_non_terminal(self):
        """Añade un símbolo no terminal"""
        symbol = self.nt_entry.get().strip()
        if symbol:
            self.nt_listbox.insert(tk.END, symbol)
            self.nt_entry.delete(0, tk.END)
    
    def _add_terminal(self):
        """Añade un símbolo terminal"""
        symbol = self.t_entry.get().strip()
        if symbol:
            self.t_listbox.insert(tk.END, symbol)
            self.t_entry.delete(0, tk.END)
    
    def _remove_non_terminal(self):
        """Elimina el símbolo no terminal seleccionado"""
        selection = self.nt_listbox.curselection()
        if selection:
            self.nt_listbox.delete(selection[0])
        else:
            messagebox.showwarning("Advertencia", "Seleccione un símbolo no terminal para eliminar")
    
    def _remove_terminal(self):
        """Elimina el símbolo terminal seleccionado"""
        selection = self.t_listbox.curselection()
        if selection:
            self.t_listbox.delete(selection[0])
        else:
            messagebox.showwarning("Advertencia", "Seleccione un símbolo terminal para eliminar")
    
    def _add_production(self):
        """Añade una producción"""
        left = self.p_left_entry.get().strip()
        right = self.p_right_entry.get().strip()
        if left and right:
            self.p_listbox.insert(tk.END, f"{left} → {right}")
            self.p_left_entry.delete(0, tk.END)
            self.p_right_entry.delete(0, tk.END)
    
    def _new_grammar(self):
        """Crea una nueva gramática"""
        self.nt_listbox.delete(0, tk.END)
        self.t_listbox.delete(0, tk.END)
        self.p_listbox.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.current_grammar = None
    
    def _build_grammar_from_ui(self) -> Grammar:
        """Construye una gramática desde los datos de la UI"""
        grammar = Grammar(self.name_entry.get().strip(), self.type_var.get())
        
        # Añadir no terminales
        for i in range(self.nt_listbox.size()):
            symbol = self.nt_listbox.get(i).strip()
            grammar.add_non_terminal(symbol)
        
        # Añadir terminales
        for i in range(self.t_listbox.size()):
            symbol = self.t_listbox.get(i).strip()
            grammar.add_terminal(symbol)
        
        # Establecer símbolo inicial
        start = self.start_entry.get().strip()
        if start:
            grammar.set_start_symbol(start)
        
        # Añadir producciones
        for i in range(self.p_listbox.size()):
            prod_str = self.p_listbox.get(i).strip()
            if '→' in prod_str:
                left, right = prod_str.split('→', 1)
                grammar.add_production(left.strip(), right.strip())
            elif '->' in prod_str:
                left, right = prod_str.split('->', 1)
                grammar.add_production(left.strip(), right.strip())
        
        return grammar
    
    def _validate_grammar(self):
        """Valida la gramática actual"""
        try:
            grammar = self._build_grammar_from_ui()
            is_valid, message = grammar.validate()
            if is_valid:
                self.current_grammar = grammar
                messagebox.showinfo("Validación", f"✓ {message}")
            else:
                messagebox.showerror("Error de Validación", message)
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar: {str(e)}")
    
    def _save_grammar(self):
        """Guarda la gramática en un archivo"""
        try:
            grammar = self._build_grammar_from_ui()
            is_valid, message = grammar.validate()
            if not is_valid:
                messagebox.showerror("Error", f"No se puede guardar: {message}")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                grammar.save_to_file(filename)
                self.current_grammar = grammar
                messagebox.showinfo("Éxito", "Gramática guardada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def _load_grammar(self):
        """Carga una gramática desde un archivo"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                grammar = Grammar.load_from_file(filename)
                self.current_grammar = grammar
                
                # Actualizar UI
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, grammar.name)
                self.type_var.set(grammar.type)
                self.start_entry.delete(0, tk.END)
                self.start_entry.insert(0, grammar.start_symbol or "")
                
                self.nt_listbox.delete(0, tk.END)
                for nt in sorted(grammar.non_terminals):
                    self.nt_listbox.insert(tk.END, nt)
                
                self.t_listbox.delete(0, tk.END)
                for t in sorted(grammar.terminals):
                    self.t_listbox.insert(tk.END, t)
                
                self.p_listbox.delete(0, tk.END)
                for left in sorted(grammar.productions.keys()):
                    for right in grammar.productions[left]:
                        self.p_listbox.insert(tk.END, f"{left} → {right}")
                
                messagebox.showinfo("Éxito", "Gramática cargada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar: {str(e)}")
    
    def _parse_string(self):
        """Analiza una cadena"""
        if not self.current_grammar:
            grammar = self._build_grammar_from_ui()
            is_valid, message = grammar.validate()
            if not is_valid:
                messagebox.showerror("Error", f"Gramática inválida: {message}")
                return
            self.current_grammar = grammar
        
        string = self.parse_entry.get().strip()
        if not string:
            messagebox.showwarning("Advertencia", "Ingrese una cadena para analizar")
            return
        
        try:
            parser = create_parser(self.current_grammar)
            is_accepted, tree = parser.parse(string)
            
            if is_accepted:
                self.result_label.config(text="✓ CADENA ACEPTADA", foreground="green")
                self.tree_text.delete(1.0, tk.END)
                self.tree_text.insert(tk.END, str(tree))
            else:
                self.result_label.config(text="✗ CADENA RECHAZADA", foreground="red")
                self.tree_text.delete(1.0, tk.END)
                self.tree_text.insert(tk.END, "No se pudo construir el árbol de derivación.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar: {str(e)}")
    
    def _generate_strings(self):
        """Genera las primeras 10 cadenas"""
        if not self.current_grammar:
            grammar = self._build_grammar_from_ui()
            is_valid, message = grammar.validate()
            if not is_valid:
                messagebox.showerror("Error", f"Gramática inválida: {message}")
                return
            self.current_grammar = grammar
        
        try:
            generator = StringGenerator(self.current_grammar)
            strings = generator.generate_strings(10)
            
            self.strings_listbox.delete(0, tk.END)
            if strings:
                for i, s in enumerate(strings, 1):
                    self.strings_listbox.insert(tk.END, f"{i}. {s}")
            else:
                self.strings_listbox.insert(tk.END, "No se pudieron generar cadenas")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar cadenas: {str(e)}")
    
    def _update_view(self):
        """Actualiza la vista de la gramática"""
        if not self.current_grammar:
            grammar = self._build_grammar_from_ui()
            is_valid, message = grammar.validate()
            if not is_valid:
                self.view_text.delete(1.0, tk.END)
                self.view_text.insert(tk.END, f"Gramática inválida: {message}")
                return
            self.current_grammar = grammar
        
        self.view_text.delete(1.0, tk.END)
        self.view_text.insert(tk.END, str(self.current_grammar))


def main():
    """Función principal"""
    root = tk.Tk()
    app = GrammarApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

