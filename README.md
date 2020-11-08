# DBNormalizer
Minimal command line python program to help you normalise your relational database design.

## Before you Run:
Modify the portion indicated in the main.py file according to comment (YES pls modify inside the source code).
The modification basically gives the following inputs:
1. Set of variables in your database.
2. List of functional dependencies implied in your database (You don't have to list trivial ones).
3. Set the normal form you want to test/achieve.

An example of the inputs will be:
```
R = ['A','B', 'C']
FD = [
    [['A', 'B'], ['C']], 
    [['A'], ['B']], 
    [['B'], ['A']]
]
normalform = normalforms.threenf
```

## How to Run:
python main.py

## Output:
(Note: Output is formated using python3. For best experience pls use python3.)

Following the previous example, the output will be:
```
all candiate keys:
[{'A'}, {'B'}]


a minimal cover:
['A'] -> ['B']
['B'] -> ['A']
['B'] -> ['C']


check normal form: threenf
['A', 'B'] -> ['C'] True
['A'] -> ['B'] True
['B'] -> ['A'] True


decomposition: threenf 
dependency-preserving
==== ['A', 'B', 'C']
['A'] -> ['B'] True
['A'] -> ['C'] True
['B'] -> ['A'] True
['B'] -> ['C'] True


synthesis: threenf 
already in 3NF
==== ['A', 'B', 'C']
['A', 'B'] -> ['C'] True
['A'] -> ['B'] True
['B'] -> ['A'] True
```
* The 1st section gives you all possible candidate keys
* The 2nd section computes the minimal cover
* The 3rd section checks if the supplied functional dependencies are normalized.
* The 4th section trys to achieve required normalization by decomposition method (can loose some dependencies).
* The 5th section trys to achieve 3NF by synthesis method (only 3NF is guaranteed, and all dependencies preserved).

Unless you must achieve BCNF, synthesis method is more popular because it at least gives you 3NF and preserves 
all original dependencies. And mostly likely, it gives you BCNF as well.

