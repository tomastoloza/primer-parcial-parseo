# Guia de Estudio: Analisis Semantico

## 1. Concepto de Analisis Semantico
- Su objetivo es comprobar que el programa fuente cumpla con las reglas de cohesion y significado definidas por el diseñador del lenguaje.
- A diferencia del analisis sintactico que analiza la estructura, el analisis semantico valida que los elementos tengan sentido en conjunto.
- Es un proceso dirigido por la sintaxis: el parser es quien invoca las acciones semanticas a medida que procesa las reglas sintacticas de la gramatica.
- En la practica, el analisis sintactico, semantico y la generacion de codigo intermedio se realizan juntos en una sola pasada.

## 2. Verificaciones Semanticas Comunes
- Compatibilidad de tipos: Verificar que los tipos de datos que intervienen en expresiones sean compatibles (ej. no sumar un entero con un booleano, o asignar un string a un float).
- Verificacion de subprogramas: Validar que la cantidad y tipo de los parametros reales provistos en una llamada coincidan con los parametros formales de la declaracion de la funcion o procedimiento.
- Retorno de funciones: Comprobar que el tipo de la expresion retornada por una funcion coincida con el tipo de retorno declarado de la misma.
- Unicidad de declaraciones: Asegurar que los identificadores de variables, constantes y subprogramas no se declaren mas de una vez dentro de un mismo ambito.

## 3. Atributos Semanticos
- Los atributos representan la informacion semantica (metadatos) asociada a los simbolos de la gramatica (tanto terminales como no terminales).
- Se puede pensar en cada simbolo como un registro y en los atributos como los campos de ese registro (ej. nombreVar.lexema, nombreVar.nombreTipo).
- Los atributos viajan por el Arbol de Analisis Sintactico.
- Tipos de atributos:
  - Atributos sintetizados: Se calculan a partir de los valores de los atributos de los hijos del nodo en el arbol. La informacion sube desde las hojas hacia la raiz.
  - Atributos heredados: Se calculan a partir de los valores de los atributos de los nodos hermanos o del padre. La informacion desciende o viaja horizontalmente en el arbol.

## 4. Acciones Semanticas
- Son fragmentos de codigo escrito en un lenguaje de programacion especifico, insertados dentro de las producciones de la gramatica.
- Tienen la funcion de manipular el valor de los atributos y realizar las comprobaciones semanticas pertinentes.
- Habitualmente se encierran entre llaves dentro de las reglas de produccion.
- Ejemplo en pseudocodigo de accion semantica para asignacion de tipo:
  ```
  DeclVar ::= var nombreVar dospuntos TipoVar puntocoma
            { nombreVar.nombreTipo = TipoVar.nombreTipo; }
  TipoVar ::= entero
            { TipoVar.nombreTipo = entero.lexema; }
          | booleano
            { TipoVar.nombreTipo = booleano.lexema; }
  ```

## 5. Esquemas de Traduccion
- Gramatica S-atribuida: Utiliza unicamente atributos sintetizados. Las acciones semanticas se colocan siempre al final de la parte derecha de las producciones. Es facil de evaluar en parsers ascendentes (como SLR).
- Gramatica L-atribuida: Admite atributos sintetizados y tambien heredados, con la condicion de que un atributo heredado de un simbolo solo dependa de atributos del padre o de simbolos hermanos situados a su izquierda. Las acciones semanticas pueden colocarse en cualquier posicion de la regla. Se puede evaluar durante el parseo descendente (LL(1)).
