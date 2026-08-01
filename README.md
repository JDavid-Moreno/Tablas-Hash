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

### Direccionamiento abierto (open addressing)

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

Para crear la tabla hash, usaremos una clase:

```
class HashTable:
    def __init__(self):
            self.capacity = 10
            self.size = 0
            self.boards = [[] for _ in range(self.capacity)]
```

Aquí como es una tabla, la capacidad o su tamaño ya está definido, en este caso elegimos 10, asi mismo, creamos otras dos variables, una para la cantidad de datos que contiene la tabla (nos ayudara con el factor de carga) que empieza en 0 y otra para crear la tabla como tal, que para este caso será una lista con listas adentro.

> [!NOTE]
> **Nota:** No se usó un diccionario, ya que técnicamente un diccionario es una tabla hash en sí, entonces estaríamos creando una tabla hash en una tabla hash, lo cual no tiene sentido, aquí creamos la tabla hash

#### Función Hash

Para la función hash, usaremos algo llamado **Polynomial rolling**, este es un algoritmo para convertir texto en un número de forma rápida. Usa potencias de un número primo y operaciones de módulo para comparar cadenas de caracteres en tiempo constante.

```
    def hash(self, key):
        sum = 0
        for i, char in enumerate(str(key)):
            sum += ord(char) * (31 ** i)
        return sum % self.capacity
```

Para este caso, primero volvemos cada letra en su valor ASCII, después cada valor lo multiplicamos por 31 (número primo) elevado a la posicion de la letra. Ejemplo, si tengo "Juan"

$ASCII(J) * 31⁰$

$ASCII(u) * 31¹$

$ASCII(a) * 31²$

$ASCII(n) * 31³$

Usamos la función `ord()` que es la que vuelve las letras en valores, y la suma de todos le sacamos él `%`, y ese valor será su índice.

#### Insertar

```
    def insert(self, key, value):
        index = self.hash(key)
        board = self.boards[index]
        for i, (k, v) in enumerate(board):
            if k == key:
                board[i] = (key, value)
                return
        board.append((key, value))
        self.size += 1

        if self.size / self.capacity > 0.75:
            self.resize()
```

Aquí primero le asignamos su índice, después recorremos la lista hasta llegar a su índice (recordemos que la tabla ya está llena, es decir, si tengo una tabla de tamaño 4, esta es `[[], [], [], []]`), una vez en su índice, la agregamos a la lista de ese índice, sin importar si hay otro elemento en ese índice.

### Buscar

```
    def search(self, key):
        index = self.hash(key)
        board = self.boards[index]

        for k, v in board:
            if k == key:
                return v

        return f"Clave {key} no encontrada"
```

Es muy parecido al anterior. Donde de igual manera, toca recorrer la lista, hasta encontrar la clave, en caso de que no, envia un mensaje de que no se encontró o no existe.

#### Eliminar

```
    def delete(self, key):
        index = self.hash(key)
        board = self.boards[index]

        for i, (k, v) in enumerate(board):
            if k == key:
                board.pop(i)
                self.size -= 1
                return
        return f"Clave {key} no encontrada"
```

Lo mismo que el anterior, recorre la tabla buscando el elemento para eliminarlo, asi mismo, decrece la cantidad de elementos para que no existan "elementos fantasma", esto para que el factor de carga no haga extender el tamaño de la tabla, y si no encuentra la clave devuelve un mensaje de que no se encontró.

#### Actualizar tamaño

```
    def resize(self):
        old_boards = self.boards
        self.capacity *= 2
        self.boards = [[] for _ in range(self.capacity)]
        self.size = 0

        for board in old_boards:
            for key, value in board:
                self.insert(key, value)
```

Generalmente, cuando se extiende una tabla, se duplica su tamaño, por lo que hacemos eso y como creamos una tabla nueva, tenemos que "mudar" todos los elementos a esa nueva tabla recalculando nuevamente sus índices, ya que al ser más grande, su cálculo dara distinto.

#### Visualizar la tabla

```
    def __repr__(self):
        result = []
        for b in self.boards:
            if b:
                result.append(b)
        return str(result)

    def view(self):
        board = self.boards
        for i in board:
            print(i, end=" ")
```

Existen 2 maneras, la primera es solo mostrando los índices que tienen elementos, esto se hace si la tabla crece mucho. Y la otra es imprimiendo la tabla como normalmente sería mostrando todos sus índices aunque estén vacíos.

### Usando Direccionamiento abierto (open addressing)

En este caso, tendremos una diferencia, y es que como aquí los elementos se van moviendo de índice en caso de que él se les asignó este ocupado, tendremos que usar otra variable.

```
class HashTable:
    def __init__(self):
        self.capacity = 10
        self.size = 0
        self.slots = [None] * self.capacity
        self.deleted = object()
```

aquí `capacity` y `size` se mantienen igual, por otro como es una tabla (tamaño definido) se rellena con `None` para definir su tamaño.

Por otro lado, `deleted` será la nueva variable que nos ayudara para evitar inconsistencias para buscar elementos, aquí `None` hace el trabajo de decir "en este índice jamás ha habido un valor", mientras que `deleted` es más como decir, aquí hubo algún elemento, esto se hace para que por ejemplo:

Juan cayó en el índice 3 y ana también, por lo que ana se va para el índice 4, por lo que en caso de que Juan sea eliminado, al buscar Ana y que nos dé índice 3, salga `deleted` de que puede que esté borrada o que este más adelante en la lista (la recorra), por otro lado, si buscamos y nos da `None`, significa que la clave jamás ha existido y para la búsqueda.

La función hash la mantendremos igual que la anterior por lo que queda exactamente igual.

#### Insertar

```
    def insert(self, key, value):
        if self.size / self.capacity >= 0.7:
            self.resize()

        index = self.hash(key)
        first_deleted = None
        for i in range(self.capacity):
            position = (index + i) % self.capacity
            slot = self.slots[position]

            if slot is None:
                goal = first_deleted if first_deleted is not None else position
                self.slots[goal] = [key, value]
                self.size += 1
                return
            if slot is self.deleted:
                if first_deleted is None:
                    first_deleted = position
                continue
            if slot[0] == key:
                slot[1] = value
                return

        return f"Tabla llena"
```

Para este caso, como no tenemos listas, sino que usamos todos los índices, tendremos que estar más pendientes del factor de carga, de igual manera le calculamos su índice, en caso de que este ocupado, vamos avanzando de manera lineal (si su índice es el 4, vamos al 5, si está ocupado al 6 y asi), él `% self.capacity` es para que en caso de que lleguemos al final se reinicie al primer índice, esto para que revise todos los índices que existen.

Si encontramos `None`, significa que puede insertar en ese índice sin problema, pero en caso de que en el camino paso por un `deleted`, se devuelve a ese índice.

#### Buscar / obtener

```
    def get(self, key):
        index = self.hash(key)
        for i in range(self.capacity):
            position = (index + i) % self.capacity
            slot = self.slots[position]

            if slot is None:
                return None
            if slot is not self.deleted and slot[0] == key:
                return slot[1]

        return None
```

Esta es muy parecida al del ejemplo anterior, se da el índice y se recorre buscando si está en dicho índice o si esta más adelante.

#### Eliminar

```
    def remove(self, key):
        index = self.hash(key)
        for i in range(self.capacity):
            position = (index + i) % self.capacity
            slot = self.slots[position]

            if slot is None:
                return False
            if slot is not self.deleted and slot[0] == key:
                self.slots[position] = self.deleted
                self.size -= 1
                return True

        return False
```

Usa la misma idea que buscar, pero baja la cantidad de elementos para que no se incremente el tamaño de la tabla sin sentido.

#### Actualizar tamaño

```
    def resize(self):
        old_slots = self.slots
        self.capacity  *= 2
        self.slots = [None] * self.capacity
        self.size = 0

        for slot in old_slots:
            if slot is not None and slot is not self.deleted:
                self.insert(slot[0], slot[1])
```

Misma idea que el ejemplo anterior, si la tala se llena, se duplica su tamaño y se mudan todos los elementos de la antigua a la nueva con sus nuevos índices.

---

## Material adicional

