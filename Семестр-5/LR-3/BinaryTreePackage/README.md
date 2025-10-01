This is a package providing recursive and iterative binary tree generators. Each nodes' values are generated using provided functions. (By default, the leaf values are equal to the root value.)
Don't take it too seriously. This package was made mainly as educational project.

# Installation
```bash
pip install binarytrees_nv
```

## Usage
```python
from binarytrees_nv import gen_bin_tree_iterative, gen_bin_tree_recursive

height: int = 4

# recursive
recursive_tree = gen_bin_tree_recursive(height)
# or iterative
iterative_tree = gen_bin_tree_iterative(height)

print(recursive_tree)
print(iterative_tree)


# Custom functions for leaf values
def left_function(x):
    return x ** 2

def right_function(x):
    return x - 2

custom_tree = gen_bin_tree_iterative(height, left_function=left_function, right_function=right_function)

print(custom_tree)
```
