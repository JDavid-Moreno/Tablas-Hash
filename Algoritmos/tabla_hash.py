class HashTable:
    def __init__(self, capacity = 10):
            self.capacity = capacity
            self.size = 0
            self.buckets = [[] for _ in range(capacity)]

    def hash(self, key):
        sum = 0
        for i, char in enumerate(str(key)):
            sum += ord(char) * (31 ** i)
        return sum % self.capacity

    def insert(self, key, value):
        index = self.hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > 0.75:
            self.resize()

    def search(self, key):
        index = self.hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v

        return f"Clave {key} no encontrada"

    def delete(self, key):
        index = self.hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return
        return f"Clave {key} no encontrada"

    def resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)

    def __repr__(self):
        result = []
        for b in self.buckets:
            if b:
                result.append(b)
        return str(result)

def main():
    board = HashTable()
    board.insert("Ana", 25)
    board.insert("Leo", 30)
    board.insert("Nao", 28)

    print(board.search("Ana"))  # 25
    board.delete("Leo")
    print(board)
main()