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

Debido a como funcionan la asignación de los índices, puede que uno o varios elementos queden con un mismo índice, eso es una **colisión**, y para solucionar tenemos 2 posibles soluciones:

### Encadenamiento (Chaining)

Esta consiste que en vez de guardar un elemento, se guarda una lista la cual contiene todos los elementos que se les asignó ese índice, esta puede ser una lista normal o una lista enlazada, como se quiera hacer.

Lo malo de este método es que si comienzan a haber varios elementos en ese índice, su complejidad podría pasar de $O(1)$ a $O(k)$, donde $k$ es el largo de la lista.

### Direccionamiento abierto (open chaining)

Todo se guarda como normalmente sería, es decir sin elementos que sean listas, para esto, si un elemento es asignado a una posición la cual ya está ocupada, este se le busca otra posición que no lo esté, esta puede ser la siguiente o hacer doble hashing (dos funciones hash por si la primera dio un índice ocupado).

Está al manejarse asi usa menos memoria, pero tiene la desventaja que la tabla se puede llenar a diferencia del método anterior, que técnicamente puede tener elementos infinitos. Por lo que, en caso de que se llene, esta tiene que crecer más. 

---

### Factor de carga

El factor de carga sirve para saber que tan frecuentes podrían ser las colisiones, esta es:

```
factor de carga = numero de elementos / tamaño del arreglo
```

Si el factor de carga crece demasiado, por ejemplo, si es mayor a $0.75$ que es default en algunos lenguajes de programación, entonces las colisiones serán muy frecuentes y el rendimiento decrece.

Para el segundo caso para colisiones, lo que hace generalmente cuando se llena o su factor de carga es muy alto, es duplicar el tamaño de la tabla y mudar todos los elementos a esa tabla, aunque baja el factor de carga "artificialmente", es muy efectivo.

---

## Implementación

### Usando Encadenamiento (Chaining)

