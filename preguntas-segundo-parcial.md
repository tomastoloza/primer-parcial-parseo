# Preguntas Evaluadas en el Segundo Parcial

De acuerdo al registro de conversaciones, el profesor evaluó las siguientes preguntas y temas:

## 1. Gramáticas y Conceptos Generales
* **¿Qué diferencia hay entre el análisis léxico y el análisis sintáctico?**
* **¿Qué es una GIC (Gramática Independiente del Contexto)?**
* **¿Qué es una producción?**
* **¿Cómo se aumenta una gramática?**

## 2. Analizadores Descendentes / LL(1)
* **¿Qué es una gramática LL(1)?**
* **¿Por qué el analizador LL(1) es top-down (descendente)?**
* **En LL(1), ¿por qué la recursión a izquierda genera problemas?**
* **En LL(1), ¿qué pasa con el conjunto de Siguientes (*Follow*) cuando hay producciones que derivan en lambda ($\lambda$ / vacío)?**
* **Explicar el conjunto de Primeros y cómo se calcula.**
* **Ejercicio práctico:** Diseñar una gramática y determinar/explicar si es LL(1).

## 3. Analizadores Ascendentes / SLR / Shift-Reduce
* **¿Qué es *shift* (desplazamiento) y cómo afecta a la pila?**
* **Explicar cada una de las operaciones de un analizador SLR.**
* **En SLR, ¿por qué se aumenta la gramática?**
* **¿Por qué se utiliza el conjunto de Siguientes (`sig()`) en el SLR?**
* **¿Qué pasa cuando se realiza un *reduce* (reducción) y qué efecto tiene en el árbol sintáctico?**

## 4. Comparativas y Detección de Errores
* **¿Cuál es más sencillo de implementar/realizar, SLR o LL(1)?**
* **¿En qué momento se detectan/pasan los errores en LL(1) y en SLR?**