class HashTable:
    def __init__(self):
        self.capacity = 10
        self.size = 0
        self.slots = [None] * self.capacity
        self.deleted = object()

    def hash(self, key):
        sum = 0
        for i, char in enumerate(str(key)):
            sum += ord(char) * (31 ** i)
        return sum % self.capacity

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

    def resize(self):
        old_slots = self.slots
        self.capacity  *= 2
        self.slots = [None] * self.capacity
        self.size = 0

        for slot in old_slots:
            if slot is not None and slot is not self.deleted:
                self.insert(slot[0], slot[1])

def main():
    tabla = HashTable()
    tabla.insert("nombre", "Juan")
    tabla.insert("edad", 25)
    print(tabla.get("nombre"))
    tabla.remove("edad")
    print(tabla.get("edad"))
main()