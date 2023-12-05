use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Instant;
use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};
use lazy_static::lazy_static;

const ALPHABET_SIZE: usize = 26;

#[derive(Default)]
struct TrieNode {
    children: [Option<Box<TrieNode>>; ALPHABET_SIZE],
    is_end_of_word: bool,
}

impl TrieNode {
    fn new() -> Self {
        Default::default()
    }
}

fn get_node() -> Box<TrieNode> {
    Box::new(TrieNode::new())
}

fn insert(root: &mut TrieNode, key: &str) {
    let mut p_crawl = root;
    for &c in key.as_bytes() {
        let index = (c - b'a') as usize;
        p_crawl = p_crawl.children[index].get_or_insert_with(|| get_node());
    }
    p_crawl.is_end_of_word = true;
}

fn search(root: &TrieNode, key: &str) -> bool {
    let mut p_crawl = root;
    for &c in key.as_bytes() {
        let index = (c - b'a') as usize;
        match &p_crawl.children[index] {
            Some(child) => p_crawl = child,
            None => return false,
        }
    }
    p_crawl.is_end_of_word
}

fn is_leaf(root: &TrieNode, key: &str) -> bool {
    let mut p_crawl = root;
    for &c in key.as_bytes() {
        let index = (c - b'a') as usize;
        match &p_crawl.children[index] {
            Some(child) => p_crawl = child,
            None => return true,
        }
    }
    p_crawl.children.iter().all(|child| child.is_none())
}

fn create_dictionary() -> Box<TrieNode> {
    let mut root = get_node();
    let file = File::open("CollinsScrabbleDictionary2019.txt").expect("Failed to open file");
    let reader = BufReader::new(file);
    for line in reader.lines() {
        let mut word = line.expect("Failed to read line");
        word.make_ascii_lowercase();
        insert(&mut root, &word);
    }
    root
}

lazy_static! {
    static ref ROOT: Box<TrieNode> = create_dictionary();
}

const DIRECTIONS: [(i32, i32); 8] = [
    (-1, 1), (0, 1), (1, 1),
    (-1, 0),          (1, 0),
    (-1, -1), (0, -1), (1, -1)
];

fn add_word(words: &Arc<Mutex<HashSet<String>>>, word: String) {
    if word.len() > 2 && search(&*ROOT, &word) {
        let mut words_set = words.lock().expect("Mutex lock failed");
        words_set.insert(word);
    }
}

fn valid_recurse(new_location: (usize, usize), visited_so_far: &Vec<(usize, usize)>, board: &Vec<Vec<String>>) -> bool {
    // Check if we're within the bounds of the board:
    if new_location.0 >= board.len() || new_location.1 >= board[0].len() || new_location.0 == 0 || new_location.1 == 0 {
        return false;
    }
    // Check if we've been to this location before
    !visited_so_far.contains(&new_location)
}

fn solve_recursive(board: Vec<Vec<String>>, visited_so_far: &mut Vec<(usize, usize)>, location: (usize, usize), word_so_far: String, words: &Arc<Mutex<HashSet<String>>>) {
    visited_so_far.push(location);
    add_word(words, word_so_far.clone());
    if is_leaf(&*ROOT, &word_so_far) {
        visited_so_far.pop();
        return;
    }
    // go in all directions
    for &direction in &DIRECTIONS {
        let new_location = ((location.0 as i32 + direction.0) as usize, (location.1 as i32 + direction.1) as usize);
        if valid_recurse(new_location, &visited_so_far, &board) {
            visited_so_far.push(new_location);
            let new_word_so_far = word_so_far.clone() + &board[new_location.0][new_location.1];
            solve_recursive(board.clone(), visited_so_far, new_location, new_word_so_far, words);
            visited_so_far.pop();
        }
    }
}

fn solve_thread(letters: Vec<Vec<String>>, row: usize, col: usize, words: &Arc<Mutex<HashSet<String>>>) {
    let mut visited_so_far = Vec::new(); // Each thread has its own visited_so_far vector
    let location = (row, col); // Each thread has its own location array
    solve_recursive(letters.clone(), &mut visited_so_far, location, letters[row][col].clone(), words);
}

fn solve(letters: Vec<Vec<String>>) -> HashSet<String> {
    let start = Instant::now();
    let words = Arc::new(Mutex::new(HashSet::new()));
    let mut threads = Vec::new();
    for row in 0..letters.len() {
        for col in 0..letters[0].len() {
            let words_clone = words.clone();
            let letters_clone = letters.clone();
            threads.push(thread::spawn(move || solve_thread(letters_clone, row, col, &words_clone)));
        }
    }

    // Wait for all threads to finish
    for thread in threads {
        thread.join().expect("Thread join failed");
    }

    let elapsed = start.elapsed();
    println!("Solving took: {} seconds", elapsed.as_secs());
    Arc::try_unwrap(words).expect("Failed to unwrap Arc").into_inner().expect("Failed to unwrap Mutex")
}

fn main() {
    let mut board = Vec::new();
    let mut line = String::new();
    std::io::stdin().read_line(&mut line).expect("Failed to read line");
    let num_lines = line.trim().parse::<usize>().expect("Failed to parse number of lines");
    for _ in 0..num_lines {
        let mut curr_line = String::new();
        std::io::stdin().read_line(&mut curr_line).expect("Failed to read line");
        let curr_line_vec: Vec<String> = curr_line.to_lowercase().split_whitespace().map(String::from).collect();
        board.push(curr_line_vec);
    }
    let words = solve(board);
    println!("Found {} Words: {:?}", words.len(), words);
}
