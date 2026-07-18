# Guia de Estudio: Parser ASDP (Analisis Sintactico Descendente Predictivo)

## 1. Conceptos Generales y GIC
- El analisis sintactico se encarga de verificar que la secuencia de tokens provista por el analizador lexico cumpla con las reglas estructurales de una Gramatica Independiente del Contexto (GIC).
- Una GIC esta definida por un conjunto de simbolos terminales, simbolos no terminales, un axioma inicial y un conjunto de producciones.
- Una produccion es una regla de reemplazo de la forma "A -> alfa", donde "A" es un simbolo no terminal y "alfa" es una cadena de terminales y no terminales.
- Aumentar una gramatica consiste en agregar un nuevo simbolo inicial (axioma primado) y una produccion de la forma "S' -> S", donde "S" es el axioma original. Esto sirve para indicar claramente el fin de la aceptacion de la cadena al llegar al final de la entrada de forma unica.

## 2. Analizador LL(1)
- El analizador LL(1) lee la entrada de izquierda a derecha (L: left-to-right) y construye una derivacion por izquierda (L: leftmost derivation) utilizando un solo simbolo de preanalisis (1: lookahead).
- Es un analizador de tipo descendente (top-down) porque comienza desde el axioma inicial de la gramatica e intenta reconstruir el arbol sintactico hacia las hojas (los terminales de la entrada).
- Para decidir que regla aplicar sin ambiguedad, requiere calcular el conjunto de prediccion de cada produccion.

## 3. Problemas de la Gramatica en LL(1)
- Recursion a izquierda: Ocurre cuando un no terminal puede derivar en una cadena que comienza con si mismo (ej. A -> A alfa). Genera bucles infinitos en algoritmos descendentes porque el parser intenta expandir el mismo simbolo indefinidamente.
- Eliminacion de recursion a izquierda:
  - Para reglas de la forma "A -> A alfa | beta" (donde beta no empieza con A).
  - Se reescribe como:
    - "A -> beta A'"
    - "A' -> alfa A' | lambda" (donde lambda representa la cadena vacia).
- Factores comunes por la izquierda: Ocurre cuando dos o mas producciones de un mismo no terminal comienzan con el mismo prefijo (ej. A -> alfa beta1 | alfa beta2). El parser no puede decidir que regla usar con un solo lookahead.
- Factorizacion a izquierda:
  - Se reescribe como:
    - "A -> alfa A'"
    - "A' -> beta1 | beta2"

## 4. Calculo de los Conjuntos de Primeros y Siguientes
- Conjunto de Primeros (PRIM):
  - Es el conjunto de simbolos terminales que pueden aparecer al inicio de las cadenas derivadas de una secuencia de simbolos.
  - Algoritmo de calculo para una produccion "A -> alfa1 alfa2 ... alfan":
    - Si la produccion es "A -> lambda", entonces PRIM(A) incluye a lambda.
    - Si alfa1 es un terminal, entonces PRIM(alfa1) es el conjunto formado por ese terminal.
    - Si alfa1 es un no terminal, se calcula PRIM(alfa1) y se agrega a PRIM(A) (excluyendo lambda).
    - Si PRIM(alfa1) contiene lambda, se analiza el siguiente simbolo (alfa2) y se agrega su PRIM (excluyendo lambda), y asi sucesivamente. Si todos los simbolos en el cuerpo pueden derivar en lambda, entonces lambda pertenece a PRIM(A).
- Conjunto de Siguientes (SIG):
  - Es el conjunto de simbolos terminales que pueden aparecer inmediatamente a la derecha de un no terminal en alguna forma sentencial.
  - Algoritmo de calculo:
    - Para el axioma inicial S, agregar el simbolo de fin de archivo "$" a SIG(S).
    - Para cada produccion de la forma "A -> alfa B beta", agregar todo lo que este en PRIM(beta) (excepto lambda) a SIG(B).
    - Si beta puede derivar en lambda (o no hay beta, es decir "A -> alfa B"), entonces agregar todo lo que este en SIG(A) a SIG(B).

## 5. Conjunto de Prediccion and Condicion LL(1)
- Conjunto de Prediccion (PRED):
  - Indica que simbolos de la entrada nos permiten elegir una produccion determinada.
  - Para una regla de la forma "A -> alfa":
    - Si lambda no pertenece a PRIM(alfa), entonces PRED(A -> alfa) es igual a PRIM(alfa).
    - Si lambda pertenece a PRIM(alfa), entonces PRED(A -> alfa) es igual a (PRIM(alfa) menos lambda) union SIG(A).
- Condicion LL(1):
  - Una gramatica es LL(1) si y solo si para cualquier no terminal A con producciones alternativas "A -> alfa1 | alfa2 | ... | alfan", los conjuntos de prediccion correspondientes son mutuamente disjuntos (su interseccion es vacia).
  - Si la interseccion de PRED de dos alternativas no es vacia, existe un conflicto y la gramatica no es LL(1).

## 6. Ejemplo Practico de Analisis LL(1)
- Gramatica de entrada:
  ```
  S -> a S T | b
  T -> c T | d
  ```
- Calculo de Primeros:
  ```
  PRIM(S) = {a, b}
  PRIM(T) = {c, d}
  ```
- Calculo de Siguientes:
  ```
  SIG(S) = {$, c, d} (S es axioma, y en "S -> a S T", a la derecha de S esta T, por ende agregamos PRIM(T) = {c, d})
  SIG(T) = {$, c, d} (En "S -> a S T", T esta al final, por lo que agregamos SIG(S))
  ```
- Calculo de Predicciones:
  ```
  PRED(S -> a S T) = PRIM(a S T) = {a}
  PRED(S -> b) = PRIM(b) = {b}
  PRED(T -> c T) = PRIM(c T) = {c}
  PRED(T -> d) = PRIM(d) = {d}
  ```
- Evaluacion de la condicion LL(1):
  - Para S: PRED(S -> a S T) interseccion PRED(S -> b) es igual a {a} interseccion {b} = vacio.
  - Para T: PRED(T -> c T) interseccion PRED(T -> d) es igual a {c} interseccion {d} = vacio.
  - Conclusion: La gramatica es LL(1).

## 7. Tabla de Analisis y Trazado con Pila
- Tabla LL(1) para el ejemplo anterior:
  ```
  +---+----------+--------+---------+--------+-------+
  |   | a        | b      | c       | d      | $     |
  +---+----------+--------+---------+--------+-------+
  | S | S -> aST | S -> b | error   | error  | error |
  | T | error    | error  | T -> cT | T -> d | error |
  +---+----------+--------+---------+--------+-------+
  ```
- Trazado de la cadena "abcdd$":
  ```
  +---------+----------+-----------------+
  | Pila    | Entrada  | Accion o Regla  |
  +---------+----------+-----------------+
  | $ S     | abcdd$   | S -> a S T      |
  | $ T S a | abcdd$   | Emparejar(a)    |
  | $ T S   | bcdd$    | S -> b          |
  | $ T b   | bcdd$    | Emparejar(b)    |
  | $ T     | cdd$     | T -> c T        |
  | $ T c   | cdd$     | Emparejar(c)    |
  | $ T     | dd$      | T -> d          |
  | $ d     | dd$      | Emparejar(d)    |
  | $       | d$       | Error (Rechazo) |
  +---------+----------+-----------------+
  ```

## 8. Deteccion de Errores
- En el parser LL(1), un error sintactico se detecta en el momento en que el simbolo en el tope de la pila no coincide con el token actual de entrada (error de emparejamiento), o bien cuando la celda correspondiente de la tabla de analisis contiene una entrada de "error".
- La deteccion ocurre de manera inmediata antes de realizar cualquier paso de expansion incorrecto sobre el token de entrada actual.

## 9. Automatas de Pila (PDA)
- Definicion: Es un modelo matematico de computacion que extiende los automatas finitos agregando una memoria auxiliar en forma de pila. Se utiliza para reconocer lenguajes independientes del contexto.
- Modelos de aceptacion:
  - Por estado final: El automata acepta la cadena si, tras consumir toda la entrada, el control se encuentra en alguno de los estados finales (o de aceptacion), sin importar que elementos queden en la pila.
  - Por vaciado de pila: El automata acepta la cadena si, tras consumir toda la entrada, la pila queda completamente vacia, independientemente del estado de control en el que se encuentre.
- Metodo sistematico de conversion de GIC a PDA:
  - Estado inicial (Q0): Se lee el primer simbolo, se apila el simbolo inicial de la pila (habitualmente el numeral "#" o "Z") y se transiciona al estado de procesamiento (Q1).
  - Estado de procesamiento (Q1):
    - Transiciones de produccion (no deterministicas): Para cada regla de la forma "A -> alfa", se define una transicion que lee "lambda" (nada), desapila "A" y apila la cadena "alfa" (manteniendo el orden izquierdo a la vista).
    - Transiciones de emparejamiento: Para cada simbolo terminal "t" del alfabeto, se define una transicion que lee "t" de la entrada, desapila "t" de la pila y no apila nada ("lambda").
  - Estado final (Q2): Se realiza una transicion al detectar el simbolo inicial de pila ("#"), desapilando dicho simbolo y transicionando al estado final (Q2) de aceptacion.
- Simulacion en herramientas: Se suele utilizar JFlap (Shift-Flap) para modelar y simular de forma interactiva el comportamiento de estos automatas y evaluar la pila ante diferentes entradas.

