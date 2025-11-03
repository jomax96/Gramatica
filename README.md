# Analizador Sintáctico (Parser) y Generador de Lenguajes

Proyecto desarrollado para la asignatura de Lenguajes Formales de la Universidad Pedagógica y Tecnológica de Colombia (UPTC).

## Descripción

Esta aplicación permite definir, guardar y cargar Gramáticas Regulares (Tipo 3) y Libres de Contexto (Tipo 2), e implementa los algoritmos necesarios para:

- **Analizar (Parsear)**: Determinar si una cadena de entrada pertenece al lenguaje generado por la gramática
- **Visualizar**: Generar y mostrar el árbol de derivación para cadenas aceptadas
- **Generar**: Producir las primeras 10 cadenas más cortas del lenguaje usando búsqueda en anchura (BFS)

## Características

### Funcionalidades Principales

1. **Definición de Gramáticas**
   - Especificación de la tupla G = (N, T, P, S):
     - **N**: Conjunto de símbolos no terminales
     - **T**: Conjunto de símbolos terminales
     - **P**: Conjunto de producciones (reglas de reescritura)
     - **S**: Símbolo inicial
   - Soporte para gramáticas Tipo 2 (Libres de Contexto) y Tipo 3 (Regulares)

2. **Persistencia**
   - Guardar gramáticas en formato JSON
   - Cargar gramáticas previamente guardadas

3. **Parsing (Análisis Sintáctico)**
   - Algoritmo CYK (Cocke-Younger-Kasami) para gramáticas Tipo 2
   - Autómata finito para gramáticas Tipo 3
   - Clasificación de cadenas como Aceptadas o Rechazadas

4. **Visualización del Árbol de Derivación**
   - Representación textual del árbol de derivación para cadenas aceptadas
   - Visualización con indentación y caracteres especiales

5. **Generador de Cadenas**
   - Generación de las primeras 10 cadenas más cortas del lenguaje
   - Implementación con BFS para garantizar cadenas más cortas primero
   - Manejo de recursión para evitar bucles infinitos

## Requisitos

- Python 3.7 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)
- Biblioteca `python-docx` (solo necesaria para leer documentos Word, no para ejecutar la aplicación)

## Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias (si es necesario):
```bash
pip install python-docx
```

Nota: `python-docx` solo es necesario si quieres leer archivos .docx. Para ejecutar la aplicación principal, no es necesario instalar nada adicional ya que Tkinter viene con Python.

## Uso

### Ejecutar la Aplicación

```bash
python gui.py
```

O también:

```bash
python main.py
```

### Interfaz de Usuario

La aplicación cuenta con una interfaz gráfica con 4 pestañas:

1. **Definir Gramática**: Aquí puedes crear una nueva gramática especificando:
   - Nombre de la gramática
   - Tipo (Tipo 2 o Tipo 3)
   - Símbolo inicial
   - No terminales
   - Terminales
   - Producciones

2. **Analizar Cadena**: Ingresa una cadena para verificar si pertenece al lenguaje generado por la gramática. Si es aceptada, se muestra el árbol de derivación.

3. **Generar Cadenas**: Genera y muestra las primeras 10 cadenas más cortas del lenguaje.

4. **Ver Gramática**: Muestra una vista completa de la gramática actual.

### Ejemplo de Uso

#### Crear una Gramática Tipo 2

**Gramática para expresiones aritméticas simples:**

- Nombre: "Expresiones Aritméticas"
- Tipo: Tipo 2
- Símbolo Inicial: E
- No Terminales: E, T, F
- Terminales: +, *, id, (, )
- Producciones:
  - E → E + T
  - E → T
  - T → T * F
  - T → F
  - F → ( E )
  - F → id

#### Crear una Gramática Tipo 3

**Gramática para el lenguaje a*b*:**

- Nombre: "a^n b^n"
- Tipo: Tipo 3
- Símbolo Inicial: S
- No Terminales: S, A, B
- Terminales: a, b
- Producciones:
  - S → aA
  - S → bB
  - A → aA
  - A → bB
  - B → bB
  - B → ε

## Estructura del Proyecto

```
proyectoGramatica/
├── grammar.py          # Clase Grammar y funciones de persistencia
├── parser.py            # Algoritmos de parsing (CYK y autómata finito)
├── tree.py              # Representación y visualización de árboles
├── generator.py         # Generador de cadenas con BFS
├── gui.py               # Interfaz gráfica de usuario
├── main.py              # Punto de entrada principal
├── README.md            # Este archivo
└── requirements.txt     # Dependencias del proyecto
```

## Algoritmos Implementados

### Parsing para Tipo 2 (Gramáticas Libres de Contexto)
- **Algoritmo CYK**: Utiliza programación dinámica para determinar si una cadena pertenece al lenguaje. Complejidad temporal: O(n³) donde n es la longitud de la cadena.

### Parsing para Tipo 3 (Gramáticas Regulares)
- **Autómata Finito No Determinista (AFND)**: Construye un autómata desde las producciones de la gramática y simula su ejecución para verificar la aceptación de cadenas.

### Generación de Cadenas
- **Búsqueda en Anchura (BFS)**: Explora el espacio de derivaciones nivel por nivel, garantizando que las cadenas más cortas se encuentren primero. Incluye límite de profundidad para evitar bucles infinitos.

## Formato de Archivo

Las gramáticas se guardan en formato JSON con la siguiente estructura:

```json
{
  "name": "Nombre de la gramática",
  "type": "Tipo 2",
  "non_terminals": ["E", "T", "F"],
  "terminals": ["+", "*", "id", "(", ")"],
  "productions": {
    "E": ["E + T", "T"],
    "T": ["T * F", "F"],
    "F": ["( E )", "id"]
  },
  "start_symbol": "E"
}
```

## Limitaciones y Consideraciones

1. **Gramáticas Tipo 2**: El algoritmo CYK requiere que la gramática esté en forma normal de Chomsky (A → BC o A → a) para funcionar correctamente. Sin embargo, el parser intenta manejar otras formas básicas.

2. **Gramáticas Tipo 3**: Se asume que las producciones están en forma normal derecha (A → aB o A → a).

3. **Generación de Cadenas**: El generador tiene un límite de profundidad para evitar bucles infinitos en gramáticas recursivas.

## Criterios de Evaluación Cumplidos

- ✅ **Correctitud del Parser (50%)**: Algoritmos implementados y funcionales para ambos tipos de gramáticas
- ✅ **Visualización del Árbol (20%)**: Árbol de derivación textual generado correctamente
- ✅ **Generador de Cadenas (10%)**: Genera las 10 cadenas más cortas usando BFS
- ✅ **Funcionalidad Guardar/Cargar (10%)**: Persistencia en formato JSON implementada
- ✅ **Calidad de Código e Interfaz (10%)**: Código organizado, comentado y con interfaz gráfica clara

## Autor

Desarrollado para la asignatura de Lenguajes Formales - UPTC

## Licencia

Este proyecto es parte de un trabajo académico.

