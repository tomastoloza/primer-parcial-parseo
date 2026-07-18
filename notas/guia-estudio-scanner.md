# Guia de Estudio: Analisis Lexico (Scanner)

## 1. Conceptos Generales del Analizador Lexico
- El scanner es la primera fase de un compilador. Su funcion principal es leer el archivo de codigo fuente caracter por caracter, agruparlos en secuencias logicas y reconocer los componentes lexicos.
- La entrada del scanner es el codigo fuente (texto plano).
- La salida del scanner es una secuencia de tokens que se entregan al analizador sintactico (parser) bajo demanda.
- El proceso es guiado por la sintaxis (parser driven): el parser le solicita al scanner el siguiente token cuando lo necesita para continuar el analisis.

## 2. Definiciones Basicas
- Token o componente lexico: Es una categoria gramatical de simbolos que representan las palabras clave, identificadores, operadores, constantes, simbolos de puntuacion y especiales de un lenguaje. Son los simbolos terminales de la GIC.
- Lexema: Es la secuencia de caracteres del codigo fuente que coincide con un patron y se asocia a un token (ej. el lexema "while" se asocia al token While, el lexema "123" se asocia al token Numero).
- Patron: Es la regla que describe los posibles lexemas de un token. Se define formalmente mediante expresiones regulares.

## 3. Expresiones Regulares Comunes
- Identificador: letra (letra | numero)*
- Numero entero: digito+
- Numero real: digito+ (. digito+)?
- Operadores: +, -, *, /, ==, !=, <=, >=

## 4. Funciones Principales del Scanner
- Administrar el archivo fuente: abrirlo, leer caracteres del buffer de entrada y cerrarlo.
- Descartar elementos irrelevantes: espacios en blanco, tabulaciones, saltos de linea y comentarios.
- Agrupar caracteres para formar lexemas y asignarles su token correspondiente.
- Retornar los tokens al parser.
- Reportar errores lexicos: identificar simbolos que no coinciden con ningun patron del lenguaje.
- Realizar el mapeo de errores indicando la linea y columna correspondientes del archivo fuente.
- Insertar identificadores en la Tabla de Simbolos (esta tarea tambien la puede realizar el parser).

## 5. Diseño e Implementacion del Scanner
- Diagrama de transiciones (DT): Representa graficamente los estados de un Automata Finito (AF) utilizado para reconocer los tokens del lenguaje.
- Diferencias entre un DT del compilador y un Automata Finito Determinista (AFD) tradicional:
  - El AFD solo indica si una cadena pertenece al lenguaje o no (acepta o rechaza). El DT del scanner lee caracteres hasta completar un lexema valido, retorna el token asociado, y deja el puntero de lectura preparado para el proximo token.
  - En un DT, cualquier transicion no definida genera un estado de error inmediato.
  - En un DT, cuando un caracter leido no coincide con la continuacion del patron pero el lexema anterior ya era valido, el automata llega a un estado de aceptacion con retroceso (indicado habitualmente con un asterisco). El puntero de lectura debe retroceder en la entrada para procesar ese caracter en el siguiente token.
- Tabla de transiciones: Es la representacion matricial del DT, donde las filas representan los estados del automata y las columnas representan las entradas o caracteres posibles. Las celdas indican el estado siguiente.

## 6. Detalles e Implementaciones Clave de Clase
- Mecanismo de Retroceso (Asterisco):
  - El scanner debe leer un caracter extra para saber que el token actual finalizo.
  - Ejemplo: Si el scanner esta leyendo el numero 25 seguido de un operador "+", lee "2", luego "5", y luego "+". Al leer "+", el automata determina que el digito termino. Se alcanza el estado de aceptacion de numero entero para "25" y se marca con un asterisco (*), indicando que el cursor de lectura de la entrada debe retroceder una posicion para que el "+" sea procesado en la siguiente peticion.
- Tratamiento de Espacios y Formato:
  - En lenguajes como Java o C, los espacios en blanco, tabulaciones y saltos de linea se descartan simplemente como separadores.
  - En lenguajes como Python, la indentacion es sintacticamente significativa. El lexer no debe descartarla, sino procesar los espacios y tabuladores iniciales de cada linea para generar tokens especiales de delimitacion de bloques, denominados INDENT y DEDENT.
- Prevencion de Fallos por Conversion Numerica:
  - Al procesar strings numericos extremadamente largos en Python, la operacion de conversion de tipo (ej: int(lexema)) podria causar excepciones o desbordamientos en memoria de maquina.
  - Como buena practica, se debe rodear la conversion con bloques de captura de excepciones (try-except) en Python. Si ocurre un error, se reporta al gestor de errores del compilador y se le asigna un valor seguro por defecto (como cero), evitando la caida inesperada del compilador.
- Automatizacion vs Diseño Manual:
  - Manual: Permite un control absoluto, optimizaciones de velocidad y facilidad para reportar errores precisos y recuperables.
  - Automatizada: Emplea herramientas generadoras de analizadores lexicos como Flex (para C/C++) o PLY/lex (para Python) a partir de un archivo con expresiones regulares, lo que simplifica sustancialmente el desarrollo a costa de menor flexibilidad en el manejo detallado de errores.

