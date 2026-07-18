# Que vamos a ver?

* Fases de un compilador
* Diseñar y desarrollar un compilador
  * Desde un metacompilador


* Patrones
* Expresiones Regulares
* GIC -> Validar sintaxis
* Produccion -> Acciones semanticas
* Verificaciones, tipos y simbolos del Lenguaje de programacion



# Traductor / Translator

* Programa que recibe un programa escrito en un lenguaje y lo traduce a otro lenguaje

# Para definir un lenguaje:
- Objetivos
- Alcance
- Especificaciones Sintacticas
- Especificaciones Semanticas
- Especificaciones Lexicas
- Que el programa tenga decisiones / bifurcaciones (if-else)
- Que el programa tenga bucles (for) (opcional)
- Que el programa permita funciones (opcional)


## Ejemplo Minimizado: "Colchita"

- **Objetivo:** Crear una colcha.
  - Contamos con dos retazos iniciales.
  - Los retazos se pueden girar y coser entre sí.
- **Alcance:** Definir un lenguaje simple para manipular retazos de tela, detallando sus reglas léxicas, sintácticas y semánticas.

## Especificaciones

### Léxicas
Se utilizan Expresiones Regulares (ER) o patrones para identificar los componentes básicos (tokens):
- Variables: `r1`, `r2` (identificadores de retazos).
- Operaciones: `girar`, `coser`.

### Sintácticas
Se define la estructura válida de las operaciones:
- `girar(retazo)` -> retorna un retazo girado.
- `coser(r1, r2)` -> retorna un retazo cosido (unión de dos retazos).

### Semánticas
Se define el significado y las reglas de validación de las operaciones:
- **`girar`**: Gira el retazo 90 grados en sentido horario.
- **`coser`**: Une dos retazos, uno al lado del otro.
  - *Validación en tiempo de ejecución:* Ambos retazos deben tener la misma altura al momento de unirlos.

## Ejemplos de Programas

### Programa 1 (Error Sintáctico)
La estructura de la instrucción no respeta el formato esperado de una invocación de función.
```text
r1 coser r2
```

### Programa 2 (Válido - OK)
La sintaxis, los componentes léxicos y la semántica son aparentemente correctos.
```text
coser(r1, r2)
```

### Programa 3 (Error Léxico/Semántico)
¿Qué es `r3`? El identificador puede fallar a nivel léxico si no encaja en la ER, o semánticamente si la variable no ha sido inicializada o declarada.
```text
coser(r3, r2)
```

### Programa 4 (Composición de operaciones - OK)
Operaciones anidadas válidas que manipulan los retazos para lograr un resultado final más complejo.
```text
girar(coser(girar(r1), girar(girar(r2))))
```