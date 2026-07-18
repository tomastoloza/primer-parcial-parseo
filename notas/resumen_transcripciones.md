# Guia de Estudio y Resumen de Clases de Parseo

## Indice de Unidades y Recursos

- Unidad 1: Introduccion a Traductores y Compiladores
  - Teoria y conceptos: [app.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/app.ipynb)
- Unidad 2: Analisis Lexico (Scanner)
  - Teoria y conceptos: [scanner.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/scanner.ipynb)
  - Transcripcion de clase: [Clase 08 (2026-04-27)](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/08_2026%2004%2027%2019%2005%2016%20PARSEO.md)
- Unidad 3: Analisis Sintactico y Automatas de Pila (PDA)
  - Teoria y conceptos: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb), [asap.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asap.ipynb), [tools.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/tools.ipynb)
  - Transcripciones de clase: [Clase 07 (2026-05-04 Parte I)](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/07_2026%2005%2004%20PARSEO%20PARTE%20I.md), [Clase 06 (2026-05-04 Parte II)](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/06_2026%2005%2004%20PARTE%20II.md), [Clase 01 (2026-05-11)](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/01_2026%2005%2011%20PARSEO.md)
- Unidad 4: Analisis Sintactico Descendente Predictivo (ASDP LL(1))
  - Teoria y conceptos: [asdp.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asdp.ipynb)
  - Transcripciones de clase: [Clase 05 (2026-06-01 Parte I)](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/05_2026%2006%2001%20PARSEO%20PARTE%20I.md), [Clase 04 (2026-06-01 Parte II)](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/04_2026%2006%2001%20PARTE%20II%20EJERCITACION.md)
- Unidad 5: Analisis Sintactico Ascendente Predictivo (ASAP SLR)
  - Teoria y conceptos: [asap.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/asap.ipynb)
  - Transcripcion de clase: [Clase 03 (2026-06-08)](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/03_2026%2006%2008%20PARSEO.md)
- Unidad 6: Tablas de Tipos, Simbolos y Analisis Semantico
  - Teoria y conceptos: [tablas.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/tablas.ipynb), [sem.ipynb](file:///Users/ttoloza/git/personal/unahur/parseo/fgl/doc/sem.ipynb)
  - Transcripcion de clase: [Clase 02 (2026-06-22)](file:///Users/ttoloza/git/personal/unahur/parseo/transcripciones/02_2026%2006%2022%20PARSEO.md)

## Unidad 1: Introduccion a Traductores y Compiladores

- Definiciones basicas de la materia:
  - Traductor: Recibe un codigo fuente en un lenguaje y lo traduce a otro lenguaje.
  - Compilador: Traduce un lenguaje de alto nivel a bajo nivel (codigo de maquina o bytecode).
  - Interprete: Ejecuta directamente las instrucciones del programa sin generar una traduccion intermedia permanente.
  - Preprocesador: Herramienta que procesa directivas y macros antes de que el codigo fuente entre al escaner.
- Vinculo con clases y aplicacion:
  - Se utiliza el lenguaje de juguete Colchita para modelar las distintas fases del analisis sintactico, lexico y semantico.

## Unidad 2: Analisis Lexico (Scanner)

- Conceptos teoricos desarrollados:
  - Lexema: La secuencia de caracteres concreta leida en el programa fuente.
  - Token: La clasificacion conceptual del lexema (ej. identificador, palabra reservada, operador, etc.).
  - Patron: La expresion regular que modela a los lexemas que pertenecen a ese token.
- Aspectos practicos discutidos en clase:
  - La controversia del espacio en blanco: Por defecto el scanner los ignora y actuan como simples separadores de tokens, pero en Python son sintacticamente significativos para determinar bloques de ejecucion.
  - Diferencias entre Diagramas de Transiciones del compilador y Automatas Finitos convencionales:
    - En el compilador, los estados finales del scanner tienen asignado un token que debe retornar.
    - Se introduce el concepto de RETROCESO (indicado con un asterisco en el diagrama). Sirve para retroceder el cursor de lectura un caracter si el ultimo caracter leido no coincide con el patron actual, dejandolo disponible para el siguiente analisis.
    - No se dibujan estados de error explicitos, sino que las transiciones no validas se derivan a la deteccion de errores lexicos.
  - Implementacion del scanner:
    - Generadores de codigo automatico (Lex, Flex, ply.lex, shlex): Traducen las expresiones regulares a automatas finitos minimos usando Thompson, Clausuras Lambda y algoritmos de clases.
    - Metodo manual o artesanal: Permite un codigo legible y mantenible por el diseñador, aunque toma mas tiempo de programacion.
  - Resolucion de desbordamientos:
    - Se discute el uso de try-except al procesar literales decimales/enteros en Python, capturando excepciones de conversion si la entrada es demasiado larga y asignando un valor neutro (como cero) con registro de error.

## Unidad 3: Analisis Sintactico y Automatas de Pila (PDA)

- Conceptos teoricos desarrollados:
  - El Parser es el orquestador principal que solicita tokens al escaner bajo demanda (Traduccion dirigida por la sintaxis).
  - Su funcion es verificar que el orden de los tokens respete la gramatica independiente del contexto (GIC) provista.
  - Gramaticas cuasi-independientes del contexto: Flexibilizan el uso del caracter vacio (lambda) en reglas distintas del axioma principal, simplificando la escritura de gramaticas pero reduciendo la eficiencia algoritmica.
- Implementacion de PDA en JFlap (Shift-Flap):
  - Formato de transiciones: caracter leido, extraer de pila -> insertar en pila.
  - El estado Q0 apila el numeral o Z (simbolo inicial de pila) de forma no determinista y va al estado de control Q1.
  - En Q1 se realizan las reducciones (saca la parte derecha de una regla y mete la parte izquierda) y los desplazamientos (lee un terminal y lo apila directamente).
  - Aceptacion de palabras: se discute la diferencia entre aceptacion por estado final (Q2) o aceptacion por vaciado de pila.
- Parsers con backtracking:
  - Evaluan todas las derivaciones posibles retrocediendo cuando hay una falla. Son muy ineficientes y no aptos para produccion.

## Unidad 4: Analisis Sintactico Descendente Predictivo (ASDP LL(1))

- Conceptos teoricos desarrollados:
  - LL(1): Lectura de izquierda a derecha (Left-to-right), derivacion por la izquierda (Leftmost derivation), y 1 token de preanalisis (Lookahead).
  - La construccion del arbol es de arriba hacia abajo (de la raiz a las hojas).
  - Prediccion: Permite saber exactamente que produccion aplicar con solo mirar el proximo token sin necesidad de adivinar o retroceder.
- Construccion de la Tabla Predictiva:
  - Algoritmo de Primeros (First): Simbolos terminales que pueden iniciar cadenas derivadas de un no terminal.
  - Algoritmo de Siguientes (Follow): Simbolos terminales que pueden aparecer a la derecha de un no terminal.
  - Algoritmo de Prediccion (Prediction): Utiliza Primeros y Siguientes para mapear las reglas a los terminales de entrada.
- Ejercitacion practica y trazado en clase:
  - Trazado paso a paso con tres columnas en las planillas: Pila (Stack), Entrada (Input) y Accion (Action).
  - Si una combinacion de no terminal en el tope de la pila y terminal en la entrada cae en una celda vacia de la tabla, se determina de inmediato que la palabra es rechazada (Reject).

## Unidad 5: Analisis Sintactico Ascendente Predictivo (ASAP SLR)

- Conceptos teoricos desarrollados:
  - Construccion de arbol de abajo hacia arriba (de las hojas a la raiz) aplicando desplazamientos (Shift) y reducciones (Reduce) basados en una derivacion mas a la derecha.
  - SLR utiliza items LR(0) representados con un punto que indica el avance en el analisis (ej. A -> alpha . beta).
  - Operaciones principales:
    - Clausura (Closure): Agrega producciones al conjunto cuando el punto esta antes de un no terminal.
    - Goto: Transiciona a un nuevo estado de items avanzando el punto sobre un simbolo de la gramatica.
  - Gramatica aumentada:
    - Se agrega la regla artificial S' -> S para lograr una aceptacion limpia (Accept) al reducir por completo al axioma original.
  - Tabla de Parsing:
    - Columna Action (para terminales): Desplazamientos (ej. d4, que coloca el estado 4 en la pila y avanza el cursor de lectura de la entrada) y Reducciones (ej. r3, que aplica la regla 3 reduciendo simbolos de la pila sin avanzar el cursor).
    - Columna Goto (para no terminales): Transiciones entre estados.
- Novedades organizativas y alertas:
  - El docente comunico en esta clase que el segundo examen parcial sera ORAL en el pizarron. Esto se debe a la deteccion de copias literales hechas con IA en el primer parcial escrito. El alumno debera ser capaz de trazar los algoritmos de parsing y explicar los pasos a mano.

## Unidad 6: Tablas de Tipos, Simbolos y Analisis Semantico

- Estructura y diseño de las tablas:
  - Tabla de Tipos (TT) y Tabla de Simbolos (TS) son compartidas y accedidas por todo el compilador.
  - Estrategias de alcance (scope):
    - Tabla unica con una columna que registre el ambito.
    - Pila de tablas (Scope Stack): Apila una nueva tabla al entrar a un bloque/procedimiento local y la desapila al salir, destruyendo las variables locales y liberando memoria.
- Estructura de la Tabla de Tipos (TT):
  - Codigo (ID unico auto-incremental).
  - Nombre (ej. integer, boolean, registro, vector).
  - Tipo base (ej. para matrices o vectores, apunta al codigo del tipo base).
  - Padre (enlace jerarquico para campos internos de un registro).
  - Dimension (1 para tipos basicos, o el tamaño de la estructura).
  - Minimo y maximo (para limites de arrays).
  - Ambito (id de scope).
- Estructura de la Tabla de Simbolos (TS):
  - Nombre (identificador de la variable o funcion).
  - Categoria (variable, funcion, parametro, constante).
  - Codigo de tipo (referencia a la fila de la Tabla de Tipos).
  - Numero de parametros (para funciones).
  - Lista de parametros (tipos ordenados de los parametros).
  - Ambito (id de scope).
- Analisis Semantico:
  - Comprobacion de tipos: Validacion de compatibilidad en expresiones (ej. verificar que se sumen tipos correctos).
  - Verificacion de firmas: Validacion de parametros reales contra formales en llamadas a metodos/funciones.
  - Atributos (ATR) y Acciones Semanticas (ACC) en la traduccion.
  - Definiciones Dirigidas por la Sintaxis (DDS) y Esquemas de Traduccion (ETDS).
- Reglas del Trabajo Practico (TP):
  - Exposicion grupal de TP fijada para el 6 de julio.
  - Requisitos de evaluacion: Exponer compartiendo pantalla, presentar el repositorio de codigo en git, mostrar casos de prueba automatizados y detallar conclusiones (fortalezas, debilidades, conflictos resueltos).
  - La calificacion es cualitativa (Aprobado/Desaprobado). Su entrega es obligatoria para aprobar la materia, pero la nota final de la cursada se promedia solo con los examenes parciales.

## Agenda y Cronograma Final

- Exposicion del Trabajo Practico: 6 de julio.
- Segundo Parcial (Modalidad Oral): 13 de julio.
- Recuperatorio (Trabajo Practico y Parciales): 20 de julio.
