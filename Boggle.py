#!/usr/bin/env python
import argparse
import random
import pickle
from Trie import Trie, TrieNode
from Solver import UniprocessorSolver, MultiprocessorSolver

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

def play(trie):
    board = Board(int(input("What size should the board be? The board will always be a square. ")))
    if args.multi:
        solver = MultiprocessorSolver(board.get2dArray(), trie)
    else:
        solver = UniprocessorSolver(board.get2dArray(), trie)
    solver.getWords()


def createTrie():
    print("Loading dictionary...")
    with open('english.dictionary', 'rb') as config_dictionary_file:
        trie = pickle.load(config_dictionary_file)
    print("Loaded, starting game.")
    return trie


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Boggle Solver", description="Creates and solves a boggle game of nxn size")
    parser.add_argument("-multi", action="store_true")
    args = parser.parse_args()
    trie = createTrie()
    play(trie)
    while input("Do you want to play again? Y or N ").upper() == "Y":
        play(trie)