# Guia de Estudio: Parser ASAP (Analisis Sintactico Ascendente Predictivo - SLR)

## 1. Conceptos Generales de ASAP
- El analisis sintactico ascendente (bottom-up) intenta construir el arbol de analisis sintactico comenzando desde las hojas (los terminales de la entrada) hacia la raiz (el axioma inicial).
- En cada paso, el parser busca reducir una subsecuencia de simbolos de la pila que coincide con la parte derecha de una regla de produccion, reemplazandola por la parte izquierda de dicha regla (su cabeza).
- Este tipo de parser se conoce tambien como Shift-Reduce (Desplazamiento-Reduccion).

## 2. Operaciones del Analizador Shift-Reduce
- Desplazamiento (Shift):
  - Consiste en tomar el siguiente token de la entrada y meterlo en la pila.
  - En la implementacion SLR, tambien se apila un estado del automata que representa el progreso del analisis.
- Reduccion (Reduce):
  - Consiste en identificar que en el tope de la pila se encuentra la parte derecha completa de una regla de produccion (llamada mango o handle).
  - Se desapilan los simbolos y estados correspondientes al tamaño de la parte derecha de la regla.
  - Luego, se calcula el estado siguiente usando la funcion Goto sobre el estado que quedo en el tope y la cabeza de la regla reducida, y se apilan dicho no terminal y el nuevo estado.
  - Esta accion equivale a subir en el arbol sintactico.
- Aceptacion (Accept):
  - Se declara que la cadena de entrada es sintacticamente valida al llegar al axioma inicial S' y al fin de archivo "$".
- Rechazo (Reject):
  - Se reporta un error sintactico si la tabla de analisis indica una accion vacia o error para el estado actual y el token actual.

## 3. Construccion de Automata de Items LR(0) y Aumento de Gramatica
- Aumentar la gramatica:
  - Siempre se aumenta la gramatica para el parser SLR.
  - Si la gramatica original es G con inicial S, se crea G' con produccion "S' -> S" e inicial S'. Esto permite que cuando el parser reduzca la regla "S' -> S", sepa que debe finalizar con exito (Accept) sin ambiguedades.
- Items LR(0):
  - Un item LR(0) es una produccion de la gramatica con un punto "." en alguna posicion de su parte derecha.
  - El punto indica que parte del cuerpo de la regla ya fue procesada (lo que esta a la izquierda del punto) y que parte falta procesar (lo que esta a la derecha del punto).
  - Ejemplo: Para "A -> X Y", los items posibles son:
    - "A -> . X Y" (esperando procesar X)
    - "A -> X . Y" (X ya procesado, esperando Y)
    - "A -> X Y ." (regla completa, lista para una reduccion)
- Clausura de un conjunto de items:
  - Si un item tiene el punto antes de un no terminal B (ej. "A -> alfa . B beta"), entonces agregamos todos los items de la forma "B -> . gamma" a ese conjunto de items. Se repite este proceso hasta que no se puedan agregar mas items.
- Transicion (Goto):
  - Dado un conjunto de items I y un simbolo X (terminal o no terminal), Goto(I, X) es la clausura del conjunto de todos los items obtenidos al mover el punto un lugar hacia la derecha despues del simbolo X en los items de I.
  - La coleccion canonica de conjuntos de items LR(0) representa los estados del automata del parser.

## 4. Construccion de la Tabla SLR y el Conjunto de Siguientes
- Para determinar cuando realizar una reduccion "Reduce R(n)" para una regla "A -> alfa" en un estado I que contiene el item "A -> alfa .":
  - Se utiliza el conjunto de Siguientes de la cabeza de la regla, es decir, SIG(A).
  - Solo colocamos la accion de reduccion R(n) en las columnas de los terminales que pertenezcan a SIG(A).
  - Esto ayuda a resolver posibles conflictos Shift-Reduce al acotar las situaciones en las que una reduccion es valida basandose en el contexto derecho del no terminal.

## 5. Ejemplo Practico de Analisis SLR
- Gramatica de entrada (aumentada):
  ```
  0) S' -> S
  1) S -> a S b
  2) S -> c
  ```
- Coleccion de conjuntos de items LR(0):
  ```
  Estado I0:
    S' -> . S
    S -> . a S b
    S -> . c

  Goto(I0, S) = Estado I1:
    S' -> S .

  Goto(I0, a) = Estado I2:
    S -> a . S b
    S -> . a S b
    S -> . c

  Goto(I0, c) = Estado I3:
    S -> c .

  Goto(I2, S) = Estado I4:
    S -> a S . b

  Goto(I2, a) = Estado I2 (bucle)
  Goto(I2, c) = Estado I3

  Goto(I4, b) = Estado I5:
    S -> a S b .
  ```
- Calculo de Siguientes:
  ```
  SIG(S') = {$}
  SIG(S) = {$, b}
  ```
- Construccion de la Tabla SLR:
  - Columnas de accion (terminales: a, b, c, $) y columnas de Goto (no terminales: S).
  - Tabla resultante:
  ```
  +--------+-----------+-----------+-----------+-----------+-------+
  | Estado | a         | b         | c         | $         | S     |
  +--------+-----------+-----------+-----------+-----------+-------+
  | 0      | Shift(2)  | error     | Shift(3)  | error     | Go(1) |
  | 1      | error     | error     | error     | Accept    | error |
  | 2      | Shift(2)  | error     | Shift(3)  | error     | Go(4) |
  | 3      | error     | Reduce(2) | error     | Reduce(2) | error |
  | 4      | error     | Shift(5)  | error     | error     | error |
  | 5      | error     | Reduce(1) | error     | Reduce(1) | error |
  +--------+-----------+-----------+-----------+-----------+-------+
  ```
  - Nota: En los estados 3 y 5, colocamos Reduce solo en las columnas pertenecientes a SIG(S) = {$, b}.

## 6. Trazado con Pila para la cadena "acb$"
- Trazado usando la tabla SLR:
  ```
  +------------------+----------+-----------------+
  | Pila de Estados  | Entrada  | Accion Realizada|
  +------------------+----------+-----------------+
  | 0                | acb$     | Shift(2)        |
  | 0 2              | cb$      | Shift(3)        |
  | 0 2 3            | b$       | Reduce(2): S->c |
  +------------------+----------+-----------------+
  ```
  - Al reducir S -> c (longitud 1):
    - Se desapila 1 estado (el 3), quedando el tope en 2.
    - Se busca Goto(2, S) que es 4.
    - Se apila el estado 4.
  ```
  +------------------+----------+-----------------+
  | Pila de Estados  | Entrada  | Accion Realizada|
  +------------------+----------+-----------------+
  | 0 2 4            | b$       | Shift(5)        |
  | 0 2 4 5          | $        | Reduce(1):S->aSb|
  +------------------+----------+-----------------+
  ```
  - Al reducir S -> a S b (longitud 3):
    - Se desapilan 3 estados (5, 4, 2), quedando el tope en 0.
    - Se busca Goto(0, S) que es 1.
    - Se apila el estado 1.
  ```
  +------------------+----------+-----------------+
  | Pila de Estados  | Entrada  | Accion Realizada|
  +------------------+----------+-----------------+
  | 0 1              | $        | Accept          |
  +------------------+----------+-----------------+
  ```

## 7. Comparativa y Deteccion de Errores: LL(1) vs SLR
- Simplicidad de implementacion:
  - LL(1) es mas sencillo de implementar recursivamente a mano (mediante funciones para cada no terminal en un parser de descenso recursivo) o con una tabla de analisis simple.
  - SLR es mas complejo de construir manualmente debido a la necesidad de calcular los conjuntos de items LR(0) y el automata, por lo que suele implementarse mediante generadores de parsers (Yacc, Bison, o herramientas de software).
- Momento de deteccion de errores:
  - El analizador sintactico LL(1) detecta un error de forma inmediata en el instante en que no puede emparejar el token actual o no hay produccion valida en la celda de la tabla.
  - El analizador SLR tambien detecta el error en el momento en que no se define transicion de Shift o Reduce para el estado y token actuales. No realiza desplazamientos invalidos erroneos, aunque puede hacer algunas reducciones antes de percatarse del error, pero nunca consumira mas simbolos de entrada incorrectos.

## 8. Analisis Sintactico Ascendente con Backtracking y modelado en JFlap
- Shift-Reduce General:
  - Antes de los analizadores deterministicos como SLR, existia el analisis ascendente general con backtracking (vuelta atras).
  - Al no tener tablas predictivas ni lookahead deterministico, el automata de pila prueba caminos de reduccion y desplazamiento de forma no determinista. Si toma un camino incorrecto, debe desarmar la pila y la entrada (backtracking), lo cual resulta computacionalmente ineficiente.
- Modelado en JFlap (Shift-Reduce):
  - Debido a que JFlap lee la pila de izquierda a derecha, se requiere una inversion de la parte derecha de las reglas de produccion (RHS) para poder ingresarlas correctamente en las transiciones de reduccion.
  - Ejemplo de inversion: Para la produccion "S -> c ( S , S )", la transicion de reduccion se ingresa en JFlap como:
    ```text
    lambda, ) S , S ( c -> S
    ```
    Esto asegura que los caracteres sean desapilados y emparejados en el orden correcto en el que quedaron en la pila.
- Secuencia de aceptacion en JFlap (Shift-Reduce):
  - Transicion Q0 a Q1: Inicializa la pila colocando el simbolo Z o numeral.
  - Estado Q1 (procesamiento):
    - Transicion de Shift: Para cada terminal t del alfabeto, lee "t" de la entrada y lo empuja a la pila (t, lambda -> t).
    - Transiciones de Reduce: Aplica las reglas invertidas (lambda, RHS_invertido -> LHS).
  - Transicion Q1 a Q2: Saca el axioma de la pila al finalizar (lambda, S -> lambda).
  - Transicion Q2 a Q3 (final): Saca el simbolo inicial de la pila (lambda, Z -> lambda) para declarar la cadena valida.

