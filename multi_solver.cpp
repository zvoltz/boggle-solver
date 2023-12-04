#include <chrono>
#include <mutex>
#include <sstream>
#include <thread>
#include "trie.h"
#include <unordered_set>
#include <vector>
using namespace std;

int directions[8][2] = {{-1, 1}, {0, 1}, {1, 1}, {-1, 0}, {1, 0}, {-1, -1}, {0, -1}, {1, -1}};

void addWord(struct TrieNode *trie, unordered_set<string>* words, string word, mutex& wordsMutex) {
    if (word.length() > 2 && search(trie, word)) {
        wordsMutex.lock();
        (*words).insert(word);
        wordsMutex.unlock();
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

void solveRecursive(struct TrieNode *trie, vector<vector<string>> board, vector<int*> visitedSoFar, int location[2], string wordSoFar, unordered_set<string>* words, mutex& wordsMutex) {
    visitedSoFar.push_back(location);
    addWord(trie, words, wordSoFar, wordsMutex);
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
            solveRecursive(trie, board, visitedSoFar, newLocation, newWordSoFar, words, wordsMutex);
            visitedSoFar.pop_back();
        }
    }
}

void solveThread(TrieNode* root, vector<vector<string>>& letters, int row, int col, unordered_set<string>* words, mutex& wordsMutex) {
    vector<int*> visitedSoFar; // Each thread has its own visitedSoFar vector
    int location[2] = {row, col}; // Each thread has its own location array
    solveRecursive(root, letters, visitedSoFar, location, letters[row][col], words, wordsMutex);
}

unordered_set<string>* solve(vector<vector<string>> letters) {
    auto start = chrono::system_clock::now();
    unordered_set<string>* words = new unordered_set<string>;
    struct TrieNode *root = create_dictionary();
    vector<thread> threads;
    mutex wordsMutex;
    for (int row = 0; row < letters.size(); row++) {
        for (int col = 0; col < letters[0].size(); col++) {
            threads.emplace_back(solveThread, root, ref(letters), row, col, words, ref(wordsMutex));
        }
    }

    // Wait for all threads to finish
    for (auto& thread : threads) {
        thread.join();
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
            new_char[0] = tolower(new_char[0]);
            if (new_char.length() > 1) {
                new_char[1] = tolower(new_char[1]);
            }
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