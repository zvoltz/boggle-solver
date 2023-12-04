#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <stdio.h>
using namespace std;

struct TrieNode;
TrieNode* create_dictionary();
bool search(struct TrieNode *root, string key);
void insert(struct TrieNode *root, string key);
bool isLeaf(struct TrieNode *root, string key);