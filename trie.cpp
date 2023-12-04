// C++ implementation of search and insert
// operations on Trie
#include "trie.h"
using namespace std;

const int ALPHABET_SIZE = 26;

// trie node
struct TrieNode
{
	struct TrieNode *children[ALPHABET_SIZE];

	// isEndOfWord is true if the node represents
	// end of a word
	bool isEndOfWord;
};

// Returns new trie node (initialized to NULLs)
struct TrieNode *getNode(void)
{
	struct TrieNode *pNode = new TrieNode;

	pNode->isEndOfWord = false;

	for (int i = 0; i < ALPHABET_SIZE; i++)
		pNode->children[i] = NULL;

	return pNode;
}

// If not present, inserts key into trie
// If the key is prefix of trie node, just
// marks leaf node
void insert(struct TrieNode *root, string key)
{
	struct TrieNode *pCrawl = root;
	for (int i = 0; i < key.length(); i++)
	{
		int index = key[i] - 'a';
		if (!pCrawl->children[index])
			pCrawl->children[index] = getNode();

		pCrawl = pCrawl->children[index];
	}
	// mark last node as leaf
	pCrawl->isEndOfWord = true;
}

// Returns true if key presents in trie, else
// false
bool search(struct TrieNode *root, string key)
{
	struct TrieNode *pCrawl = root;

	for (int i = 0; i < key.length(); i++)
	{
		int index = key[i] - 'a';
		if (!pCrawl->children[index])
			return false;

		pCrawl = pCrawl->children[index];
	}

	return (pCrawl->isEndOfWord);
}

// Returns true if there's no children and this word ends on a leaf node
bool isLeaf(struct TrieNode *root, string key)
{
	struct TrieNode *pCrawl = root;

	for (int i = 0; i < key.length(); i++)
	{
		int index = key[i] - 'a';
		if (!pCrawl->children[index])
			return true;

		pCrawl = pCrawl->children[index];
	}

	for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (pCrawl->children[i]) {
            return false;
        }
    }
    return true;
}

struct TrieNode* create_dictionary()
{
    struct TrieNode *root = getNode();
	ifstream input_file("CollinsScrabbleDictionary2019.txt");
    assert(input_file.is_open());
    string line;
    getline(input_file, line);
    while (!input_file.rdstate()) {
        transform(line.begin(), line.end(), line.begin(), [](unsigned char c){ return tolower(c); });
        insert(root, line);
        getline(input_file, line);
    }
    transform(line.begin(), line.end(), line.begin(), [](unsigned char c){ return tolower(c); });
    insert(root, line);
    input_file.close();

    return root;
}