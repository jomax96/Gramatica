from grammar import Grammar
from parser import create_parser
from generator import StringGenerator

# Cargar la gramática
grammar = Grammar.load_from_file("punto2.json")
print("=" * 60)
print(f"Gramática: {grammar.name}")
print(f"Tipo: {grammar.type}")
print(f"Símbolo Inicial: {grammar.start_symbol}")
print("\nProducciones:")
for left in sorted(grammar.productions.keys()):
    for right in grammar.productions[left]:
        print(f"  {left} → {right}")
print("=" * 60)

# Validar
is_valid, message = grammar.validate()
print(f"\nValidación: {message}")

if is_valid:
    # Crear parser
    parser = create_parser(grammar)
    
    # Probar algunas cadenas
    print("\n" + "=" * 60)
    print("PRUEBAS DE PARSING:")
    print("=" * 60)
    
    test_strings = ["a", "b", "aa", "ab", "ba", "bb", "aaa", "aab", "aba", "abb", "baa", "bab", "bba", "bbb"]
    
    for test in test_strings:
        result = parser.parse(test)
        status = "✓ ACEPTADA" if result[0] else "✗ RECHAZADA"
        print(f"  '{test}': {status}")
    
    # Generar cadenas
    print("\n" + "=" * 60)
    print("GENERACIÓN DE CADENAS (primeras 10 más cortas):")
    print("=" * 60)
    
    generator = StringGenerator(grammar)
    strings = generator.generate_strings(10)
    
    if strings:
        for i, s in enumerate(strings, 1):
            print(f"  {i}. {s}")
    else:
        print("  No se pudieron generar cadenas")

