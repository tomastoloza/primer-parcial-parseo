# Guia de Estudio: Generacion de Codigo y Codigo Intermedio

## 1. Concepto de Generacion de Codigo
- Es la fase final del proceso de traduccion. Toma la representacion intermedia del programa fuente y la traduce en codigo objeto (habitualmente codigo assembler o lenguaje de maquina).
- Para dar portabilidad al compilador, se suele generar una representacion intermedia llamada Codigo Intermedio (CI) antes de producir el codigo de maquina definitivo.

## 2. Codigo Intermedio (CI)
- Representa el comportamiento del programa de una forma mas abstracta, independiente del hardware o maquina destino.
- Beneficios del CI:
  - Permite reutilizar el mismo analizador (front-end) para construir compiladores para distintas arquitecturas de procesador (back-end).
  - Facilita la implementacion de optimizaciones de codigo independientes de la maquina.

## 3. Tipos de Representacion de Codigo Intermedio
- Codigo de tres direcciones:
  - Formato de representacion donde cada instruccion posee como maximo tres direcciones o variables (dos operandos y un resultado).
  - Se implementa comunmente mediante cuadruplas (registros con campos: Instruccion, Operando 1, Operando 2, Resultado).
  - Utiliza variables temporales creadas por el compilador para almacenar resultados parciales de la evaluacion de expresiones (ej. temp1, temp2).
  - Ejemplo para evaluar "x = x + y - 2":
    - ADD x, y, temp1
    - SUB temp1, 2, temp2
    - MOVE temp2, , x
- Codigo de maquina virtual de pila:
  - Utiliza una estructura de pila (stack) para evaluar expresiones y almacenar valores temporales.
  - La asignacion o evaluacion de operaciones desapila los valores necesarios de la pila, aplica el operador y apila el resultado.
  - Es el esquema basico usado en maquinas virtuales como la JVM (Java Virtual Machine) o P-Code.
  - Ejemplo para evaluar "x = x + y - 2" en pila:
    - apilar(x)
    - apilar(y)
    - sumar
    - apilar(2)
    - restar
    - asignar(x)
  - Aunque es facil de generar, es mas complejo traducir codigo de pila a codigo assembler de registros en maquinas reales, por lo que en la practica suele preferirse el codigo de tres direcciones.

## 4. Generacion de CI para Expresiones y Asignaciones
- Evaluacion de expresiones:
  - El compilador calcula la direccion de memoria relativa de las variables (guardada en su entrada de la Tabla de Simbolos) y genera las cuadruplas correspondientes.
  - Se utilizan temporales globales para almacenar los pasos intermedios.
  - Cada cuadrupla de tres direcciones es traducida posteriormente a instrucciones de lenguaje ensamblador especificas de la maquina (ej. MOVE, ADD, SUB).
