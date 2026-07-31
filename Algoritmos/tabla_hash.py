class HashTable:
    def __init__(self):
            self.capacity = 10
            self.size = 0
            self.boards = [[] for _ in range(self.capacity)]

    def hash(self, key):
        sum = 0
        for i, char in enumerate(str(key)):
            sum += ord(char) * (31 ** i)
        return sum % self.capacity

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

    def search(self, key):
        index = self.hash(key)
        board = self.boards[index]

        for k, v in board:
            if k == key:
                return v

        return f"Clave {key} no encontrada"

    def delete(self, key):
        index = self.hash(key)
        board = self.boards[index]

        for i, (k, v) in enumerate(board):
            if k == key:
                board.pop(i)
                self.size -= 1
                return
        return f"Clave {key} no encontrada"

    def resize(self):
        old_boards = self.boards
        self.capacity *= 2
        self.boards = [[] for _ in range(self.capacity)]
        self.size = 0

        for board in old_boards:
            for key, value in board:
                self.insert(key, value)

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

def main():
    board = HashTable()
    board.insert("Ana", 25)
    board.insert("Leo", 30)
    board.insert("Nao", 28)
    board.insert("Zoe", 30)

    print(board.search("Ana"))
    board.delete("Leo")
    print(board)
    board.view()
main()