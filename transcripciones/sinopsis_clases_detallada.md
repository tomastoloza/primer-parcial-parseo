# Guia de Estudio Detallada de Parseo: Conceptos y Algoritmos de Clase

Este documento compila en detalle los conceptos teoricos, algoritmos, ejercicios y discusiones metodologicas extraidas de las transcripciones de las clases, alineandolos con los notebooks de la carpeta [fgl/doc/](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc).

## 1. Analisis Lexico (Scanner)
- Relacion teorica: [scanner.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/scanner.ipynb)
- Clase de referencia: [08_2026 04 27 19 05 16 PARSEO.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/08_2026%2004%2027%2019%2005%2016%20PARSEO.md)

### Conceptos Fundamentales
- Lexema: Es la secuencia de caracteres que se encuentra literalmente en el codigo fuente (ej: caja_de_ahorro, 45, +).
- Token: Es la clasificacion lexicografica del lexema (ej: identificador, numero, operador_suma).
- Patron: Expresion regular asociada al token que describe que secuencias de caracteres son validas (ej: letra seguida de letras o digitos).

### Diagramas de Transiciones con Retroceso
- En un automata finito teorico, la entrada es aceptada si se llega al final y se esta en estado final.
- En un compilador, el scanner lee caracteres de un buffer y retorna un token cuando llega a un estado de aceptacion.
- Retroceso (representado con un asterisco *): Ocurre cuando el scanner lee un caracter que no pertenece al token actual sino al siguiente. El cursor de lectura de la entrada debe retroceder una posicion para que ese caracter sea procesado en la siguiente invocacion.
- Ejemplo: Para detectar el numero 25 y el operador +, el scanner lee 2, luego 5 (aun es numero), luego lee +. Como + no es un digito, el scanner transiciona al estado final de numero entero, devuelve el token entero para el lexema 25, y retrocede el cursor para dejar el + disponible para la proxima lectura.

### Implementacion y Buenas Practicas
- Tratamiento de espacios en blanco: Son controversiales. La mayoria de los lenguajes (como Java) los descartan como simples separadores. En lenguajes como Python, la indentacion (espacios y tabuladores) es sintacticamente significativa para delimitar bloques, por lo que el lexer debe convertirlos en tokens especiales (ej: INDENT, DEDENT).
- Prevencion de errores en Python: Se utiliza try-except en Python al parsear numeros muy largos que exceden la precision de la maquina (desbordamiento). Si la conversion de tipo lanza un error, el lexer captura la excepcion, asigna un valor por defecto (como cero) e informa al gestor de errores en lugar de hacer caer el compilador.
- Deteccion de errores lexicos: Identificadores que inician con digito, caracteres ilegales no declarados en el alfabeto o palabras clave mal escritas.

---

## 2. Analisis Sintactico y Automatas de Pila (PDA)
- Relacion teorica: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)
- Clases de referencia: [07_2026 05 04 PARSEO PARTE I.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/07_2026%2005%2004%20PARSEO%20PARTE%20I.md) y [06_2026 05 04 PARTE II.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/06_2026%2005%2004%20PARTE%20II.md)

### Rol del Parser
- Es el orquestador de la fase inicial de compilacion. Pide tokens al scanner de manera dirigida por la sintaxis (Parser Driver) y genera un Arbol de Analisis Sintactico (AST) que decora con reglas semanticas.
- Gramatica cuasi-independiente del contexto: Flexibiliza la inclusion de producciones lambda (vacias) en no terminales que no son el axioma principal. Simplifica la escritura de gramaticas pero reduce la eficiencia teorica del automata.

### Modelos de Automatas de Pila
- Aceptacion por estado final: El automata transiciona a un estado final habiendo consumido la entrada, sin importar el contenido de la pila.
- Aceptacion por vaciado de pila: El automata acepta la cadena si al terminar de leer la entrada la pila queda vacia.
- Metodo de conversion de GIC a PDA:
  - Estado Q0 (inicial) apila el simbolo inicial de pila (numeral o Z) y transiciona a Q1 (estado de control).
  - En Q1, para cada produccion A -> alfa se define una transicion lambda, A -> alfa (desapila A, apila alfa).
  - En Q1, para cada terminal t se define una transicion t, t -> lambda (emparejamiento).
  - Transicion de aceptacion de Q1 a Q2 (final) sacando el numeral o Z de la pila.

---

## 3. Analisis Sintactico Ascendente con Backtracking (Shift-Reduce)
- Relacion teorica: [asap.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asap.ipynb)
- Clase de referencia: [01_2026 05 11 PARSEO.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/01_2026%2005%2011%20PARSEO.md)

### Funcionamiento de Shift-Reduce
- Reconstruye el arbol sintactico desde abajo hacia arriba (de las hojas a la raiz).
- Utiliza dos operaciones principales:
  - Desplazamiento (Shift): Lee un terminal de la entrada y lo pone en la pila.
  - Reduccion (Reduce): Si el tope de la pila coincide con la parte derecha de una regla (RHS), lo reemplaza por el no terminal de la parte izquierda (LHS).

### Implementacion de Shift-Reduce en JFlap
- Inversion de reglas: JFlap procesa la pila de izquierda a derecha. Por lo tanto, para una regla S -> C ( S , S ) se debe ingresar la transicion en el automata de forma invertida:
```text
lambda, ) S , S ( C -> S
```
- Esto garantiza que al desapilar los elementos en el orden de ejecucion (primero el parentesis de cierre, luego S, etc.), se reduzca correctamente a S.
- Pasos de aceptacion:
  - Q0 a Q1: Inicializa pila con numeral/Z.
  - Q1: Realiza todas las transiciones de Shift (ej: t, lambda -> t) y las transiciones de Reduce de forma no determinista.
  - Q1 a Q2: Si el tope de la pila es el axioma S, lo saca (lambda, S -> lambda).
  - Q2 a Q3 (final): Saca el simbolo inicial Z (lambda, Z -> lambda).
- Ineficiencia: Debido a que es con backtracking, el automata debe probar todas las combinaciones posibles de shift y reduce. Si toma un camino incorrecto, debe desarmar la pila y la entrada (backtrack), lo que causa una performance prohibitiva en compiladores de produccion.

---

## 4. Analisis Sintactico Descendente Predictivo (ASDP LL(1))
- Relacion teorica: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)
- Clases de referencia: [05_2026 06 01 PARSEO PARTE I.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/05_2026%2006%2001%20PARSEO%20PARTE%20I.md), [04_2026 06 01 PARTE II EJERCITACION.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/04_2026%2006%2001%20PARTE%20II%20EJERCITACION.md) y [03_2026 06 08 PARSEO.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/03_2026%2006%2008%20PARSEO.md)

### Concepto LL(1)
- L: Left-to-right (lectura de izquierda a derecha).
- L: Leftmost derivation (derivacion mas a la izquierda).
- 1: Un unico token de lookahead para predecir que regla aplicar de manera determinista, eliminando el backtracking.

### Algoritmos de Primeros (First) y Siguientes (Follow)

Reglas de Primeros para un simbolo X:
- Si X es terminal, First(X) = {X}.
- Si X -> lambda es una produccion, entonces lambda esta en First(X).
- Si X es no terminal y X -> Y1 Y2 ... Yk, entonces se agrega First(Y1) - {lambda} a First(X). Si First(Y1) contiene lambda, se agrega First(Y2) - {lambda}, y asi sucesivamente. Si todos los Yi contienen lambda, se agrega lambda a First(X).

Reglas de Siguientes para un no terminal A:
- Si A es el axioma de la gramatica, se agrega pesos ($) a Follow(A).
- Si hay una produccion X -> alfa A beta, se agrega First(beta) - {lambda} a Follow(A).
- Si hay una produccion X -> alfa A, o X -> alfa A beta donde First(beta) contiene lambda, se agrega Follow(X) a Follow(A).

### Calculo de Predicciones
Para cada produccion A -> alfa:
- Si lambda no pertenece a First(alfa), Prediction(A -> alfa) = First(alfa).
- Si lambda pertenece a First(alfa), Prediction(A -> alfa) = (First(alfa) - {lambda}) unio Follow(A).

### Verificacion de Gramatica LL(1)
- Para toda regla alternativa del mismo no terminal (ej: A -> beta1 | beta2), la interseccion de sus predicciones debe ser vacia:
```text
Prediction(A -> beta1) interseccion Prediction(A -> beta2) = vacio
```
- Si la interseccion no es vacia, la gramatica presenta conflictos (ambiguedad o necesidad de mas lookahead) y no es LL(1).

### Ejemplo de Trazado de Parsing Predictivo
Para una gramatica con tabla predictiva armada, el parseo se traza usando tres columnas:
1. Pila (Stack): Contiene simbolos sintacticos, iniciados con pesos y el axioma (ej: $ S).
2. Entrada (Input): Contiene la cadena de tokens a validar finalizada con pesos (ej: a b c $).
3. Accion (Action): Describe si se aplica una regla o se empareja un terminal.
- Si el tope de la pila es un no terminal y el token de entrada cae en una celda vacia de la tabla predictiva, se produce un error sintactico inmediato (Reject).

---

## 5. Tabla de Tipos, Tabla de Simbolos y Semantica
- Relacion teorica: [tablas.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/tablas.ipynb) y [sem.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/sem.ipynb)
- Clase de referencia: [02_2026 06 22 PARSEO.md](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/02_2026%2006%2022%20PARSEO.md)

### Diseños de Alcance (Scope)
- Tabla unica con columna de ambito: Se mantiene una sola tabla y se agrega una columna Ambito (ej: 0 para global, 1 para P1). Al finalizar un procedimiento local, se deben borrar explicitamente todas las filas correspondientes a ese ambito para liberar memoria.
- Pila de tablas (Scope Stack): Se apila una nueva tabla independiente al ingresar a un ambito local. Las busquedas de variables se realizan desde el tope (local) hacia la base (global). Al salir del ambito, se desapila la tabla local, lo que destruye de manera limpia todas sus variables.

### Estructura de la Tabla de Tipos (TT)
Contiene la definicion de los tipos validos del lenguaje (cargando los tipos basicos como integer y boolean al iniciar):
- Codigo: Identificador entero incremental unico.
- Nombre: Nombre del tipo (ej: integer, boolean, registro, vector).
- Tipo base: Si es un vector, apunta al codigo del tipo que contiene (ej: si es vector de integer, apunta al codigo de integer).
- Padre: Si es un campo de un registro, apunta al codigo del registro contenedor.
- Dimension: 1 para tipos basicos, o la cantidad de elementos/campos para vectores o registros.
- Minimo / Maximo: Limites inferior y superior para vectores.
- Ambito: Identificador del scope actual.

### Estructura de la Tabla de Simbolos (TS)
Contiene la definicion de las variables, constantes y subprogramas declarados:
- Nombre: Identificador del simbolo.
- Categoria: Indica si es variable, constante, parametro, funcion o procedimiento.
- Codigo de tipo: Enlace al codigo correspondiente en la Tabla de Tipos.
- Numero de parametros: Para funciones y procedimientos.
- Lista de parametros: Tipos y orden de los parametros esperados.
- Ambito: Scope de declaracion.

### Analisis Semantico
- Comprobacion de tipos: Valida que los operadores reciban operandos compatibles (ej: no sumar un boolean con un integer).
- Verificacion de firmas: Valida que las llamadas a funciones tengan la cantidad y los tipos correctos de parametros reales comparados con los declarados en la TS.
- Atributos semanticos:
  - Sintetizados: El valor del atributo en un nodo se calcula a partir de los valores de sus nodos hijos (Bottom-up).
  - Heredados: El valor del atributo en un nodo se calcula a partir de sus nodos hermanos y su nodo padre (Top-down o lateral).
