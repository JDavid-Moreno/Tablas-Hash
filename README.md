# Tablas Hash 

---

Una tabla hash es una estructura que permite almacenar pares, usando `clave: valor`, por ejemplo:

```
{
    "Juan": 20
    "Ana": 18
    "Camilo": 27
} 
```
Y si, los diccionarios de python en sí son tablas hash.

Por lo que, al ser un diccionario, la mayor parte de sus operaciones como insertar o eliminar son de $O(1)$ en promedio, a diferencia de otras estructuras que son de complejidad $O(n)$ o $O(log(n))$.

---

## La función hash

La función hash consiste en tomar una clave (sin importar su tipo: String, int, float, etc.) y la convierte en un entero. Este entero se usa como índice dentro del arreglo interno. 

Por ejemplo, digamos que tenemos `"Juan"` como clave, y su función hash nos da 14 (se puede hacer de varias maneras como asignando un valor a cada letra del abecedario o usando los valores ASCII, entre otros) y el tamaño de la tabla es de 10, hacemos `14 % 10 = 4`, o sea que a la clave `Juan` le corresponde el índice 4.

### ¿Por qué se hace asi?

La idea de la función hash es que no se necesita recordar ni buscar donde se guardó un elemento, ya que se puede recalcular en el momento que se necesite dicha clave, es como una fórmula que solo buscando la clave, nos da el índice automáticamente solo haciendo un cálculo.

De esta manera, es que las inserciones, búsquedas o eliminaciones son de $O(1)$ y no de $O(n)$ como las típicas con índices, en estas debemos recorrer la lista, lo que lo hace menos eficiente a comparación que con la función hash.

Asi si queremos saber buscar por ejemplo `"Ana"`, no toca recorrer nada, sino solo recalcular la función que hicimos y nos devuelve el índice, y como la función es un cálculo, este siempre nos dara el mismo valor, por lo que no abría problemas de errores de índices.

### Como se decide el índice

En sí no hay una unica manera de definir como calcular un índice, depende de que función hash se realice, pero la manera más común que se hace es:

* si la función ya es un número entero, convertirlo a un número más grande.
* si es un String, generalmente lo que se hace es volver todos sus letras en su valor ASCII y sumar cada valor hasta que quede un unico resultado.

Después de eso, se le aplica el operador módulo `%` con el tamaño de la tabla para que el resultado quede siempre dentro del rango de la tabla (de $0$ a $n - 1$).

Pero al final del día, el criterio es el mismo: obtener una manera que distribuya las claves lo más parejo posible, para que haya la mayor cantidad de colisiones posibles.

---

## Colisiones

