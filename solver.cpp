#include <chrono>
#include <sstream>
#include "trie.h"
#include <unordered_set>
#include <vector>
using namespace std;

int directions[8][2] = {{-1, 1}, {0, 1}, {1, 1}, {-1, 0}, {1, 0}, {-1, -1}, {0, -1}, {1, -1}};

void addWord(struct TrieNode *trie, unordered_set<string>* words, string word) {
    if (word.length() > 2 && search(trie, word)) {
        (*words).insert(word);
    }
}

bool validRecurse(int newLocation[2], vector<int*> visitedSoFar, vector<vector<string>> board) {
    // Check if we're within the bounds of the board:
    if (newLocation[0] >= board.size() || newLocation[1] >= board[0].size() || 
        newLocation[0] < 0 || newLocation[1] < 0) {
        return false;
    }
    // Check if we've been to this location before
    for (int i = 0; i < visitedSoFar.size(); i++) {
        if (visitedSoFar[i][0] == newLocation[0] & visitedSoFar[i][1] == newLocation[1]) {
            return false;
        }
    }
    return true;
}

void solveRecursive(struct TrieNode *trie, vector<vector<string>> board, vector<int*> visitedSoFar, int location[2], string wordSoFar, unordered_set<string>* words) {
    visitedSoFar.push_back(location);
    addWord(trie, words, wordSoFar);
    if (isLeaf(trie, wordSoFar)) {
        visitedSoFar.pop_back();
        return;
    }
    // go in all directions
    for (int i = 0; i < 8; i++) {
        int newLocation[2] = {location[0] + directions[i][0], location[1] + directions[i][1]};
        if (validRecurse(newLocation, visitedSoFar, board)) {
            visitedSoFar.push_back(newLocation);
            string newWordSoFar = wordSoFar + board[newLocation[0]][newLocation[1]];
            solveRecursive(trie, board, visitedSoFar, newLocation, newWordSoFar, words);
            visitedSoFar.pop_back();
        }
    }
}

unordered_set<string>* solve(vector<vector<string>> letters) {
    auto start = chrono::system_clock::now();
    unordered_set<string>* words = new unordered_set<string>;
    struct TrieNode *root = create_dictionary();
    vector<int*> visitedSoFar;
    for (int row = 0; row < letters.size(); row++) {
        for (int col = 0; col < letters[0].size(); col++) {
            int location[2] = {row, col};
            solveRecursive(root, letters, visitedSoFar, location, letters[row][col], words);
        }
    }
    auto elapsed = chrono::duration_cast<std::chrono::seconds>(start.time_since_epoch());
    cout << "Solving took: " << elapsed.count() << endl;
    return words;
}

int main() {
    vector<vector<string>> board;
    string line;
    cin >> line;
    int num_lines = stoi(line);
    for (int i = 0; i < num_lines; i++) {       
        string new_char;
        vector<string> curr_line;
        for(int j = 0; j < num_lines; j++) {
            cin >> new_char;
            curr_line.push_back(new_char);
        }
        board.push_back(curr_line);
    }
    unordered_set<string>* words = solve(board);
    cout << "Found " << (*words).size() << " Words: ";
    for (string word : *words) {
        cout << word << ", ";
    }
    return 0;
}