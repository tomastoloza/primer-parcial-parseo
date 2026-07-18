# Guia de Estudio: Tablas de Tipos y de Simbolos

## 1. Introduccion a las Tablas del Compilador
- Los lenguajes de programacion permiten definir tipos primitivos, crear nuevos tipos de datos y declarar variables o subprogramas (simbolos).
- Para gestionar toda esta informacion durante las fases de compilacion, se utilizan dos estructuras de datos principales: la Tabla de Tipos (TT) y la Tabla de Simbolos (TS).
- Ambas tablas deben estar accesibles de manera constante por las fases de analisis semantico y generacion de codigo.

## 2. Tabla de Tipos (TT)
- Su funcion es almacenar la definicion de todos los tipos de datos existentes en el programa, tanto los predefinidos (primitivos como entero, booleano, real) como los definidos por el usuario (arreglos, registros, clases).
- Esencial para realizar chequeos de compatibilidad semantica.
- Campos minimos de una entrada en la Tabla de Tipos:
  - Codigo / Identificador: Un numero entero unico que identifica al tipo de dato.
  - Nombre: El nombre asignado al tipo (ej. "integer", "vector").
  - TipoBase: Para tipos compuestos, hace referencia al codigo del tipo del que esta compuesto (ej. para un arreglo de enteros, el TipoBase es el codigo de entero).
  - Padre: Utilizado en registros o clases para indicar el tipo contenedor al que pertenece.
  - Dimension: El numero de elementos si es un tipo compuesto (ej. para un arreglo de 10 elementos, la dimension es 10). Para tipos basicos, la dimension es 1.
  - Minimo: El limite inferior de un rango (ej. indice inicial de un arreglo).
  - Maximo: El limite superior de un rango (ej. indice final de un arreglo).
  - Ambito: El nivel o bloque de ejecucion donde se declaro el tipo de dato.

## 3. Tabla de Simbolos (TS)
- Almacena la informacion sobre los identificadores de variables, constantes y subprogramas creados por el programador.
- Campos basicos de una entrada en la Tabla de Simbolos:
  - Nombre / Lexema: El identificador del simbolo (ej. "x", "calcularSuma").
  - Tipo: El codigo del tipo de dato del simbolo, que apunta a una entrada en la Tabla de Tipos.
  - Categoria: Indica si es una variable, constante, funcion, procedimiento, parametro, etc.
  - Direccion / Desplazamiento: La ubicacion relativa de memoria asignada al simbolo.
  - Ambito: El nivel de anidamiento o bloque de ejecucion donde el simbolo es visible.

## 4. Gestion de Ambitos (Scopes)
- En la mayoria de los lenguajes existen ambitos anidados (ej. variables globales vs variables locales a un procedimiento).
- Regla de resolucion de nombres: Cuando se busca un simbolo o tipo, la busqueda comienza en el ambito mas interno (local) y avanza progresivamente hacia los ambitos mas externos (globales) hasta encontrar la definicion.
- Estrategias de implementacion para ambitos:
  - Tabla unica con marca de ambito: Se mantiene una unica tabla global de simbolos y tipos. Cada fila incluye una columna de Ambito (ej: 0 para global, 1 para procedimiento). Al finalizar la compilacion de un procedimiento local, el compilador debe ejecutar una operacion de limpieza para borrar explicitamente de la tabla todas las filas que correspondan a ese ambito local para liberar memoria.
  - Pila de tablas (Scope Stack): Se mantiene una pila donde se apila una nueva tabla independiente de tipo hash cada vez que se ingresa a un ambito local. Las busquedas se realizan desde el tope de la pila (ambito local mas cercano) hacia abajo (base global). Al salir del ambito, simplemente se desapila la tabla local, lo que destruye de manera limpia todas sus variables y libera memoria de forma automatica y transparente.
- Estructura eficiente: Debido al gran volumen de busquedas y accesos, se suelen implementar utilizando Tablas Hash, garantizando tiempos de acceso optimos.

## 5. Columnas Adicionales de la TS para Subprogramas
- Ademas de las variables simples, la Tabla de Simbolos debe registrar la firma de funciones y procedimientos para permitir la comprobacion semantica en sus llamadas:
  - Numero de parametros: Almacena la cantidad de parametros formales declarados.
  - Lista de parametros: Contiene la secuencia ordenada de los codigos de tipo de cada parametro formal. Esto sirve para contrastar que en la llamada se provean parametros con tipos y en orden compatibles.

