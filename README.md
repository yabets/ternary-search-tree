# Ternary Search Tree

A ternary search tree has nodes with the following attributes:
* a character, can be `None`;
* a Boolean flag that indicates whether the character represented
  by this node has been the last in a string that was inserted in the
  tree;
* the "less-than" child;
* the "equals" child and
* the "larger-than" child.

The data structure should support the following operations:
* string insert
* string search
* prefix string search
* return the number of strings stored in the data structure
* return all strings stored in the data structure

# Implementation
We implemented two classes, one to represent a node of ternary search tree, the second to represent the ternary search tree. TernarySearchTree is exported from the module ad will be used by users. Node class is only for internal usage.

### Time Complexity
`insert` has linear time complexity O(n) for n will be length of the word. For each character, it traverses or create a node in ternary search tree. The comparison and insert happen in constant time. 
`search` is faster as on every character, we go left or right. So time complexity is O(log n). 
`all_string`, `__len__` and `__repr__` uses dfs traversal to collect all words by visiting all nodes. The time complexity for these methods is O(n). 
### Space Complexity
`TernarySearchTree` uses one node per character with three child nodes. For N words of average length L, the space complexity is O(N*L)
### Best case and worst case comparisons
- In the base case scenario, strings share long prefixes and the tree is balanced. In this case, for average length L, insert is O(L) and search is O(log L).
- In average case scenarios a randomized word will create a balanced tree with insert operation O(L) for L average word length and search operation O(log L) 
- In the worst case scenario, where a tree is skewed and string rarely have shared long prefixes. The tree heigh grows and time complexity for insert O(N*L) for N words with average L length. 


# Example usage

The data structure has been implemented as a class.

```python
from ternary_search_tree import TernarySearchTree
```

Create a new empty ternery search tree.


```python
tst = TernarySearchTree()
```

Insert the string `'abc'` into the tree.


```python
tst.insert('abc')
```

Display the tree.


```python
print(tst)
```

    terminates: False
    _gt  char: a, terminates: False
    _eq    char: b, terminates: False
    _eq      char: c, terminates: True
    

Insert another string `'aqt'`.


```python
tst.insert('aqt')
```


```python
print(tst)
```

    terminates: False
    _gt  char: a, terminates: False
    _eq    char: b, terminates: False
    _eq      char: c, terminates: True
    _gt      char: q, terminates: False
    _eq        char: t, terminates: True
    

The tree should now contain two strings.


```python
len(tst)
```




    2




```python
tst.all_strings()
```




    ['abc', 'aqt']



Search for the string `'ab'`, it should be found since it is a prefix of `'abc'`.


```python
tst.search('ab')
```




    True



The string `'ac'` should not be found.


```python
tst.search('ac')
```




    False



The tree can also contain the empty string.


```python
tst.insert('')
```


```python
len(tst)
```




    3




```python
print(tst)
```

    terminates: True
    _gt  char: a, terminates: False
    _eq    char: b, terminates: False
    _eq      char: c, terminates: True
    _gt      char: q, terminates: False
    _eq        char: t, terminates: True
    


```python
tst.all_strings()
```




    ['', 'abc', 'aqt']



# Testing

The file `data/search_trees/insert_words.txt` contains words that we can insert into a tree.


```python
tst = TernarySearchTree()
with open('data/search_trees/insert_words.txt') as file:
    words = [
        line.strip() for line in file
    ]
for word in words:
    tst.insert(word)
unique_words = set(words)
```

Verify the length of the data stucture.


```python
assert len(tst) == len(unique_words), \
       f'{len(tst)} in tree, expected {len(unique_words)}'
```

Verify that all words that were inserted can be found.


```python
for word in unique_words:
    assert tst.search(word), f'{word} not found'
```

Verify that all prefixes can be found.


```python
for word in unique_words:
    for i in range(len(word) - 1, 0, -1):
        prefix = word[:i]
        assert tst.search(prefix), f'{prefix} not found'
```

Chack that when searching for a exact match, only the inserted words are found, and no prefixes.


```python
for word in unique_words:
    for i in range(len(word), 0, -1):
        prefix = word[:i]
        if prefix not in unique_words:
            assert not tst.search(prefix, exact=True), \
                   f'{prefix} found'
```

Check that the empty string is in the tree (since it is a prefix of any string).


```python
assert tst.search(''), 'empty string not found'
```

Check that the empty string is not in the tree for an exact search.


```python
assert not tst.search('', exact=True), 'empty string found'
```

Check that words in the file `data/search_trees/not_insert_words.txt` can not be found in the tree.


```python
with open('data/search_trees/not_insert_words.txt') as file:
    for line in file:
        word = line.strip()
        assert not tst.search(word), f'{word} should not be found'
```

Check that all strings are returned.


```python
all_strings = tst.all_strings()
assert len(all_strings) == len(unique_words), \
       f'{len(all_strings)} words, expected {len(unique_words)}'
assert sorted(all_strings) == sorted(unique_words), 'words do not match'
```

If not output was generated, all tests have passed.

# Performance

To assess the performance, i.e., the time it takes to insert a new string or search the ternary search tree as a function of the tree's size, we need a large dataset. This is provided in data/search_trees/corncob_lowercase.txt. This file contains over 58,000 English words, all lower case.


```python
with open('data/search_trees/corncob_lowercase.txt') as file:
    words = [line.strip() for line in file]
```


```python
len(words)
```




    58110




```python
import random
import time
```


```python
sizes = [100, 500, 1_000, 5_000, 10_000, 20_000, 30_000, 40_000, 50_000]
```


```python
samples = [
    random.sample(words, k=size) for size in sizes
]
```

We can now time how long it takes to insert words into a Ternary Search Tree of various sizes. First we build the TST based on the sample, and then we insert words.


```python
nr_runs = 10
times = {}
insert_sample = random.sample(words, k=20)
for sample in samples:
    tst = TernarySearchTree()
    for word in sample:
        tst.insert(word)
    times[len(sample)] = 0.0
    for _ in range(nr_runs):
        start_time = time.time_ns()
        for word in insert_sample:
            tst.insert(word)
        end_time = time.time_ns()
        times[len(sample)] += end_time - start_time
    times[len(sample)] /= nr_runs*1_000_000.0
times
```




    {100: 0.03317,
     500: 0.03344,
     1000: 0.03344,
     5000: 0.0392,
     10000: 0.05372,
     20000: 0.0402,
     30000: 0.27226,
     40000: 0.04001,
     50000: 0.04228}




```python
import matplotlib.pyplot as plt
```


```python
plt.plot(times.keys(), times.values());
```


    
![png](README_files/test_57_0.png)
    


We can do the same for searching words in a B-tree of various sizes. First we build the B-tree based on the sample, and then we search words.


```python
nr_runs = 10
times = {}
search_sample = random.sample(words, k=20)
for sample in samples:
    tst = TernarySearchTree()
    for word in sample:
        tst.insert(word)
    times[len(sample)] = 0.0
    for _ in range(nr_runs):
        start_time = time.time_ns()
        for word in search_sample:
            tst.search(word)
        end_time = time.time_ns()
        times[len(sample)] += end_time - start_time
    times[len(sample)] /= nr_runs*1_000_000.0
times
```




    {100: 0.01296,
     500: 0.01525,
     1000: 0.01645,
     5000: 0.02379,
     10000: 0.02642,
     20000: 0.0282,
     30000: 0.0298,
     40000: 0.02937,
     50000: 0.03081}




```python
plt.plot(times.keys(), times.values());
```


    
![png](README_files/test_60_0.png)
    



```python
nr_runs = 10
times = {}
for sample in samples:
    tst = TernarySearchTree()
    for word in sample:
        tst.insert(word)
    times[len(sample)] = 0.0
    for _ in range(nr_runs):
        search_sample = random.sample(sample, k=20)
        start_time = time.time_ns()
        for word in search_sample:
            tst.search(word)
        end_time = time.time_ns()
        times[len(sample)] += end_time - start_time
    times[len(sample)] /= nr_runs*1_000_000.0
times
```




    {100: 0.02509,
     500: 0.02522,
     1000: 0.0249,
     5000: 0.03406,
     10000: 0.04029,
     20000: 0.03555,
     30000: 0.03795,
     40000: 0.04146,
     50000: 0.04211}




```python
plt.plot(times.keys(), times.values());
```


    
![png](README_files/test_62_0.png)
    


## Comparison with Btree


```python
from ternary_search_tree import Btree
```


```python
with open('data/search_trees/corncob_lowercase.txt') as file:
    words = [line.strip() for line in file]
random.shuffle(words)
```


```python
hold_out_sample = words[-100:]
insert_sample = words[:-100]
```


```python
%%timeit
btree = Btree()
for word in insert_sample:
    btree.insert(word)
```

    119 ms ± 4.8 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    


```python
%%timeit
tst = TernarySearchTree()
for word in insert_sample:
    tst.insert(word)
```

    168 ms ± 6.84 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    


```python
word_btree = Btree()
for word in insert_sample:
    word_btree.insert(word)
```


```python
%%timeit
total = 0
for word in hold_out_sample:
    if word_btree.search(word):
        total += 1
```

    171 μs ± 3.31 μs per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
    


```python
word_tst = TernarySearchTree()
for word in insert_sample:
    word_tst.insert(word)
```


```python
%%timeit
total = 0
for word in hold_out_sample:
    if word_tst.search(word):
        total += 1
```

    136 μs ± 2.26 μs per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
    

Btree performs better on inserts compared to our TernarySearchTree. TernarySearchTree performs better on search
