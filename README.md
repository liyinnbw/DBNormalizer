# DBNormalizer
Minimal command line python program to help you normalise your relational database design.

## How to Run:
`python main.py`

The program will prompt you to enter the **attributes**, **FDs** and the **normal form type**.

## Output:
(Note: Output is formatted using python3. For best experience pls use python3.)

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
* The 4th section tries to achieve required normalization by the decomposition method (can lose some dependencies).
* The 5th section tries to achieve 3NF by synthesis method (only 3NF is guaranteed, and all dependencies preserved).

Unless you must achieve BCNF, the synthesis method is more popular because it at least gives you 3NF and preserves 
all original dependencies. And mostly likely, it gives you BCNF as well.

