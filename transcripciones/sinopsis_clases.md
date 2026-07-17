# Sinopsis de Clases de Formalizacion de Lenguajes

Este documento presenta una sinopsis de las clases dictadas, estableciendo su correspondencia con las unidades y notebooks de documentacion oficial.

## Indice Cronologico de Clases y Notebooks Asociados

1. Clase 8 (2026-04-27) - Analisis Lexico (Scanner)
   - Archivo de clase: [08_2026 04 27 19 05 16 PARSEO.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/08_2026%2004%2027%2019%2005%2016%20PARSEO.md)
   - Notebook teorico: [scanner.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/scanner.ipynb)

2. Clase 7 (2026-05-04 Parte I) - Introduccion al Analisis Sintactico y PDA
   - Archivo de clase: [07_2026 05 04 PARSEO PARTE I.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/07_2026%2005%2004%20PARSEO%20PARTE%20I.md)
   - Notebook teorico: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)

3. Clase 6 (2026-05-04 Parte II) - Ejercitacion de Automatas de Pila
   - Archivo de clase: [06_2026 05 04 PARTE II.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/06_2026%2005%2004%20PARTE%20II.md)
   - Notebook teorico: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)

4. Clase 1 (2026-05-11) - Analisis Sintactico Ascendente con Backtracking
   - Archivo de clase: [01_2026 05 11 PARSEO.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/01_2026%2005%2011%20PARSEO.md)
   - Notebook teorico: [asap.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asap.ipynb)

5. Clase 5 (2026-06-01 Parte I) - ASDP LL(1) Conceptos Teoricos
   - Archivo de clase: [05_2026 06 01 PARSEO PARTE I.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/05_2026%2006%2001%20PARSEO%20PARTE%20I.md)
   - Notebook teorico: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)

6. Clase 4 (2026-06-01 Parte II) - Ejercitacion y Trazado de ASDP LL(1)
   - Archivo de clase: [04_2026 06 01 PARTE II EJERCITACION.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/04_2026%2006%2001%20PARTE%20II%20EJERCITACION.md)
   - Notebook teorico: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)

7. Clase 3 (2026-06-08) - Resolucion de dudas de ASDP LL(1)
   - Archivo de clase: [03_2026 06 08 PARSEO.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/03_2026%2006%2008%20PARSEO.md)
   - Notebook teorico: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)

8. Clase 2 (2026-06-22) - Tabla de Tipos, Tabla de Simbolos y Semantica
   - Archivo de clase: [02_2026 06 22 PARSEO.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/02_2026%2006%2022%20PARSEO.md)
   - Notebooks teoricos: [tablas.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/tablas.ipynb) y [sem.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/sem.ipynb)

## Sinopsis Detallada de Contenidos

### Clase 8: Analisis Lexico (Scanner)
- Notebook: [scanner.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/scanner.ipynb)
- Temas principales:
  - Definicion de Lexema (cadena real leida), Token (categoria conceptual) y Patron (expresion regular).
  - Estructura del diagramas de transiciones de compiladores: se asocian retornos de tokens a los estados finales y se incluye el mecanismo de retroceso (asterisco) para devolver caracteres sobrantes a la entrada.
  - Funciones del scanner: gestionar archivos fuente, eliminar comentarios y espacios en blanco irrelevantes, y proveer tokens al parser bajo demanda.
  - Manejo de excepciones en Python (try-except) al procesar conversiones string-to-number para evitar desbordamientos de buffer por exceso de digitos.
  - Comparacion de implementacion automatica (generadores como Flex, PLY/lex) frente al diseño manual.

### Clase 7: Introduccion al Analisis Sintactico y PDA
- Notebook: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)
- Temas principales:
  - El Parser como orquestador del compilador que pide tokens al scanner mediante traduccion dirigida por la sintaxis.
  - Gramaticas Independientes del Contexto (GIC) para modelar la sintaxis de lenguajes de programacion.
  - Automatas de Pila (PDA): conceptos basicos de transiciones que leen, desapilan y apilan simbolos.
  - Criterios de aceptacion: por estado final vs por vaciado de pila.
  - Algoritmo de conversion sistematico de una gramatica GIC a un automata de pila.

### Clase 6: Ejercitacion de Automatas de Pila
- Notebook: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)
- Temas principales:
  - Modelado y simulacion en JFlap (Shift-Flap).
  - Trazado de derivaciones de cadenas validas y rechazo de cadenas invalidas.
  - Detalles de transiciones no deterministicas para el control de la pila.

### Clase 1: Analisis Sintactico Ascendente con Backtracking
- Notebook: [asap.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asap.ipynb)
- Temas principales:
  - Concepto de Bottom-up parsing: construir el arbol de analisis sintactico desde las hojas (terminales) hasta la raiz (axioma).
  - Derivaciones mas a la derecha en sentido inverso (derivaciones LR).
  - Acciones de Desplazamiento (Shift) y Reduccion (Reduce).
  - Implementacion en JFlap: exigencia de invertir la parte derecha de la produccion antes de ingresarla en la transicion de la pila para su correcto procesamiento.
  - Limitacion de performance debido al retroceso constante (backtracking) al evaluar multiples caminos de reduccion.

### Clase 5: ASDP LL(1) Conceptos Teoricos
- Notebook: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)
- Temas principales:
  - Parsing predictivo descendente para lograr una validacion de complejidad lineal sin backtracking.
  - Significado de LL(1): Left-to-right scanning, Leftmost derivation, 1 lookahead token.
  - Requisitos de la gramatica: eliminacion de recursividad a la izquierda y factorizacion a la izquierda.
  - Algoritmo para el calculo del conjunto de Primeros (First) y Siguientes (Follow).

### Clase 4: Ejercitacion y Trazado de ASDP LL(1)
- Notebook: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)
- Temas principales:
  - Llenado de la Tabla Predictiva a partir de los conjuntos de Primeros y Siguientes.
  - Trazado paso a paso del parser usando planillas de tres columnas: Pila, Entrada y Accion.
  - Criterio de rechazo de cadenas ante celdas vacias de la tabla.

### Clase 3: Resolucion de dudas de ASDP LL(1)
- Notebook: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)
- Temas principales:
  - Calculo de conjuntos de Prediccion para cada regla de produccion.
  - Condicion LL(1): la interseccion de los conjuntos de prediccion de reglas alternativas de un mismo no terminal debe dar conjunto vacio.
  - Analisis de conflictos y metodos para resolver ambiguedades de gramaticas.

### Clase 2: Tabla de Tipos, Tabla de Simbolos y Semantica
- Notebooks: [tablas.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/tablas.ipynb) y [sem.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/sem.ipynb)
- Temas principales:
  - Gestion del alcance de variables (scopes/ambitos).
  - Diseños de almacenamiento: tabla unica con columna de ambito vs pila de tablas (scope stack) para apilar y desapilar ambitos locales.
  - Tabla de Tipos: columnas basicas como Codigo, Nombre, Tipo Base, Padre, Dimension, Minimo, Maximo y Ambito.
  - Tabla de Simbolos: columnas basicas como Nombre, Categoria, Codigo de Tipo (referencia a la tabla de tipos), Numero de Parametros, Lista de Parametros y Ambito.
  - Analisis Semantico: validacion de tipos en expresiones y coincidencia de firmas en invocaciones de subprogramas.
  - Atributos semanticos: Synthesized vs Inherited.
