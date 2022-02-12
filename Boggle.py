#!/usr/bin/env python
import random
import pickle
import time
from Trie import Trie, TrieNode


class Board:
    def __init__(self, length):
        self.length = length
        self.allLetters = []
        option = int(input("Type 1 to type your own letters or 2 for the program to generate some. "))
        self.askBoard() if option == 1 else self.makeBoard()
        self.changeQs()

    def askBoard(self):
        option = int(input("Type 1 to type all letters at once or 2 to type them a row at a time. "))
        self.askAllLetters() if option == 1 else self.askAllRows()

    def askAllLetters(self):
        size = self.length * self.length
        letters = list(input(f"Type all {size} letters at once without spaces. ").upper())
        # ensure correct number of letters
        while len(letters) != size:
            letters = list(input(
                    f"{len(letters)}/{size} letters provided. Type all {size} letters at once. ").upper())
        self.separateLines(letters)

    def askAllRows(self):
        for row in range(self.length):
            self.allLetters.append(self.askOneRow(row + 1))

    def askOneRow(self, row):
        letters = input(f"Type the {self.length} letters of row {row}. ").upper()
        # ensure correct number of letters
        while len(letters) != self.length:
            letters = input(
                f"{len(letters)}/{self.length} letters provided. Type the {self.length} letters of row {row}. ")
        return list(letters.upper())

    def get2dArray(self):
        return self.allLetters

    def makeBoard(self):
        letters = self.getLettersClassic() if self.length == 4 else self.getLetters()
        self.separateLines(letters)
        return self.allLetters

    # changes a 1D array of characters into a square 2D array, assuming the given letters are the correct length
    def separateLines(self, letters):
        for i in range(self.length):
            self.allLetters.append(letters[i * self.length:(i + 1) * self.length])

    # uses letter frequencies to fill in the board
    def getLetters(self):
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']
        frequencies = [12, 1, 5, 6, 19, 4, 3, 5, 11, 1, 1, 5, 4, 11, 11, 4, 1, 12, 9, 13, 4, 1, 2, 1, 3, 1]
        letters = random.choices(population=alphabet, weights=frequencies, k=self.length * self.length)
        return letters

    # uses the redesigned letter cubes, made in 1987, only works for 4x4 boards
    def getLettersClassic(self):
        kStandardCubes = [
            "AAEEGN", "ABBJOO", "ACHOPS", "AFFKPS",
            "AOOTTW", "CIMOTU", "DEILRX", "DELRVY",
            "DISTTY", "EEGHNW", "EEINSU", "EHRTVW",
            "EIOSST", "ELRTTY", "HIMNQU", "HLNNRZ"
        ]
        letters = []
        for i in range(self.length * self.length):
            letters.append(random.choice(list(kStandardCubes[i])))
        random.shuffle(letters)
        return letters

    # since Qs only come in Qus in boggle, we need to adjust them
    def changeQs(self):
        for row in self.allLetters:
            for col in range(len(row)):
                if row[col] == 'Q':
                    row[col] = 'Qu'


class Solver:

    def __init__(self, board):
        global trie
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


def play():
    board = Board(int(input("What size should the board be? The board will always be a square. ")))
    solver = Solver(board.get2dArray())
    solver.getWords()


def createTrie():
    global trie
    print("Loading dictionary...")
    with open('english.dictionary', 'rb') as config_dictionary_file:
        trie = pickle.load(config_dictionary_file)
    print("Loaded, starting game.")


if __name__ == '__main__':
    createTrie()
    play()
    while input("Do you want to play again? Y or N ").upper() == "Y":
        play()
