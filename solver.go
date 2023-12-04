package main

import (
	"fmt"
	"sync"
	"time"
)

// AddWord adds a word to the trie
func AddWord(trie *Trie, words *sync.Map, word string) {
	if len(word) > 2 && trie.SearchWord(word) {
		words.Store(word, true)
	}
}

// ValidRecurse checks if the next move is valid on the board
func ValidRecurse(newLocation [2]int, visitedSoFar map[[2]int]bool, board [][]string) bool {
	// Check if we're within the bounds of the board:
	if newLocation[0] >= len(board) || newLocation[1] >= len(board[0]) ||
		newLocation[0] < 0 || newLocation[1] < 0 {
		return false
	}

	// Check if we've been to this location before
	return !visitedSoFar[newLocation]
}

// SolveRecursive is a recursive function to find words on the board
func SolveRecursive(trie *Trie, board [][]string, visitedSoFar map[[2]int]bool, location [2]int, wordSoFar string, words *sync.Map) {
	visitedSoFar[location] = true
	AddWord(trie, words, wordSoFar)

	if trie.isLeaf(wordSoFar) {
		delete(visitedSoFar, location)
		return
	}

	// Go in all directions
	directions := [8][2]int{{-1, 1}, {0, 1}, {1, 1}, {-1, 0}, {1, 0}, {-1, -1}, {0, -1}, {1, -1}}
	for _, direction := range directions {
		newLocation := [2]int{location[0] + direction[0], location[1] + direction[1]}
		if ValidRecurse(newLocation, visitedSoFar, board) {
			visitedSoFar[newLocation] = true
			newWordSoFar := wordSoFar + board[newLocation[0]][newLocation[1]]
			SolveRecursive(trie, board, visitedSoFar, newLocation, newWordSoFar, words)
			delete(visitedSoFar, newLocation)
		}
	}
}

// SolveThread is a goroutine for solving the board in a threaded manner
func SolveThread(root *Trie, letters [][]string, row, col int, words *sync.Map, wg *sync.WaitGroup) {
	defer wg.Done()
	visitedSoFar := make(map[[2]int]bool)
	location := [2]int{row, col}
	SolveRecursive(root, letters, visitedSoFar, location, letters[row][col], words)
}

// Solve solves the board and returns the set of found words
func Solve(letters [][]string) *sync.Map {
	start := time.Now()
	words := new(sync.Map)
	root := NewTrie()
	root.populate()
	var wg sync.WaitGroup

	for row := 0; row < len(letters); row++ {
		for col := 0; col < len(letters[0]); col++ {
			wg.Add(1)
			go SolveThread(root, letters, row, col, words, &wg)
		}
	}

	wg.Wait()
	elapsed := time.Since(start)
	fmt.Printf("Solving took: %s\n", elapsed)
	return words
}

func main() {
	var numLines int
	fmt.Scan(&numLines)
	var board [][]string
	for i := 0; i < numLines; i++ {
		var newChar string
		var currLine []string
		for j := 0; j < numLines; j++ {
			fmt.Scan(&newChar)
			currLine = append(currLine, newChar)
		}
		board = append(board, currLine)
	}
	words := Solve(board)

	word_list := []string{}
	words.Range(func(key, value interface{}) bool {
		word_list = append(word_list, key.(string))
		return true
	})
	fmt.Printf("Found %d Words: ", len(word_list))
	for _, element := range word_list {
		fmt.Printf(element + ", ")
	}
}
