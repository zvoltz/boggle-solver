import time
import multiprocessing as mp

class UniprocessorSolver:

    def __init__(self, board, trie):
        self.words = []
        self.board = board
        self.visitedSoFar = []
        self.dirs = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]
        self.trie = trie
        self.solve()

    def solve(self):
        currTime = time.perf_counter()
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.solveRecursive([row, col], self.board[row][col])
        print("Solving took: ", time.perf_counter() - currTime)
        return self.words

    # go through every possible combination of letters to find all words
    def solveRecursive(self, location, wordSoFar):
        self.visitedSoFar.append(location)
        self.addWord(wordSoFar)
        if self.isLeaf(wordSoFar, location):
            return
        for direction in self.dirs:
            self.goInDirection(location, direction, wordSoFar)
        self.visitedSoFar.remove(location)

    def addWord(self, word):
        # Boggle words must be longer than 2 letters, a real word, and cannot repeat
        if len(word) > 2 and self.trie.search(word.lower()) and word not in self.words:
            self.words.append(word.upper())

    # checks if the given path of nodes leads to a leaf, if it does, there's no more words possible,
    # and we can stop searching, also removes the location from visitedSoFar
    def isLeaf(self, word, location):
        if self.trie.isLeaf(word.lower()):
            self.visitedSoFar.remove(location)
            return True
        return False

    def getNewLocation(self, location, direction):
        newX = location[0] + direction[0]
        newY = location[1] + direction[1]
        return [newX, newY]

    # checks if the new location has been visited and if the row and column are between 0 and the length of the board
    def validRecurse(self, newLocation):
        if newLocation in self.visitedSoFar:
            return False
        if len(self.board) > newLocation[0] >= 0:
            if len(self.board[newLocation[0]]) > newLocation[1] >= 0:
                return True
        return False

    # recurse in the given direction
    def goInDirection(self, location, direction, wordSoFar):
        newLocation = self.getNewLocation(location, direction)
        if self.validRecurse(newLocation):
            self.solveRecursive(newLocation, wordSoFar + self.board[newLocation[0]][newLocation[1]])

    def getWords(self):
        for row in self.board:
            print(row)
        # sort by length then alphabetically
        self.words.sort()
        self.words.sort(reverse=True, key=len)
        print(f"Found {len(self.words)} words: ")
        print(self.words)

class MultiprocessorSolver:
    def __init__(self, board, trie):
        self.trie = trie
        self.board = board
        self.visitedSoFar = []
        self.dirs = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]
        self.word_set = set()
        self.solve()

    def solve(self):
        currTime = time.perf_counter()
        words = mp.Queue()
        word_set = set()
        solveRecursiveParameters = [([row, col], self.board[row][col], words) for row in range(len(self.board)) for col in range(len(self.board[0]))]
        processes = [mp.Process(target=self.startProcess, args=(solveRecursiveParameters[i],)) for i in range(len(self.board) * len(self.board[0]))]
        for process in processes:
            process.start()
        while True:
            try:
                word_set.add(words.get(True, 2))
            except:
                break
        for process in processes:
            process.join()
            process.terminate()
        print("Solving took: ", time.perf_counter() - currTime)

        while True:
            try:
                word_set.add(words.get(False))
            except:
                break
        self.word_set = word_set

    
    def startProcess(self, parameters):
        self.solveRecursive(*parameters)

    # go through every possible combination of letters to find all words
    def solveRecursive(self, location, wordSoFar, words):
        self.visitedSoFar.append(location)
        self.addWord(wordSoFar, words)
        if self.isLeaf(wordSoFar, location):
            return
        for direction in self.dirs:
            self.goInDirection(location, direction, wordSoFar, words)
        self.visitedSoFar.remove(location)

    def addWord(self, word, words):
        # Boggle words must be longer than 2 letters, a real word, and cannot repeat
        if len(word) > 2 and self.trie.search(word.lower()):
            words.put(word.upper())

    # checks if the given path of nodes leads to a leaf, if it does, there's no more words possible,
    # and we can stop searching, also removes the location from visitedSoFar
    def isLeaf(self, word, location):
        if self.trie.isLeaf(word.lower()):
            self.visitedSoFar.remove(location)
            return True
        return False

    def getNewLocation(self, location, direction):
        newX = location[0] + direction[0]
        newY = location[1] + direction[1]
        return [newX, newY]

    # checks if the new location has been visited and if the row and column are between 0 and the length of the board
    def validRecurse(self, newLocation):
        if newLocation in self.visitedSoFar:
            return False
        if len(self.board) > newLocation[0] >= 0:
            if len(self.board[newLocation[0]]) > newLocation[1] >= 0:
                return True
        return False

    # recurse in the given direction
    def goInDirection(self, location, direction, wordSoFar, words):
        newLocation = self.getNewLocation(location, direction)
        if self.validRecurse(newLocation):
            self.solveRecursive(newLocation, wordSoFar + self.board[newLocation[0]][newLocation[1]], words)

    def getWords(self):
        for row in self.board:
            print(row)
        # sort by length then alphabetically
        sorted_words = sorted(self.word_set, key=lambda x: (-len(x), x),)
        print(f"Found {len(self.word_set)} words: ")
        print(sorted_words)