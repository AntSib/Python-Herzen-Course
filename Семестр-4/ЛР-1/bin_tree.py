from collections import deque
from bin_tree_exceptions import InvalidTreeHeight, InvalidTreeRoot, InvalidTreeFunctions

# parameters
height: int = 6
root: int = 5
left_leaf_function = lambda x: x ** 2
right_leaf_function = lambda x: x - 2

# for debugging with prints
height_test: int = 3


def gen_bin_tree_recursive(height: int = 6, root: int = 5, left_function = lambda x: x ** 2, right_function = lambda x: x - 2):
    """
    This function generates a binary tree recursively given a height and a root node.
    
    :param height: The height of the tree.
    :param root: The root node of the tree.
    :param left_function: The function to generate the left leaf of the tree. Default is lambda x: x ** 2.
    :param right_function: The function to generate the right leaf of the tree. Default is lambda x: x - 2.

    :return: The generated binary tree. If height is 0 or less, returns None.
    """
    if not isinstance(height, int):
        raise InvalidTreeHeight(height)
    if not isinstance(root, int):
        raise InvalidTreeRoot(root)
    if height <= 0:
        return None
    
    if not callable(left_function) or not callable(right_function):
        raise InvalidTreeFunctions(left_function, right_function)

    left_leaf:  int = left_leaf_function(root)
    right_leaf: int = right_leaf_function(root)

    return {
        str(root): [
            gen_bin_tree_recursive(height - 1, left_leaf),
            gen_bin_tree_recursive(height - 1, right_leaf)
        ]
    }


def gen_bin_tree_iterative(height: int = 6, root: int = 5, left_function = lambda x: x ** 2, right_function = lambda x: x - 2):
    """
    Generates a binary tree iteratively given a height and a root node.

    :param height: The height of the tree. Must be a non-negative integer.
    :param root: The root node of the tree. Must be an integer.
    :param left_function: The function to generate the left leaf of the tree. Default is lambda x: x ** 2.
    :param right_function: The function to generate the right leaf of the tree. Default is lambda x: x - 2.

    :raises InvalidTreeHeight: If the height is not an integer.
    :raises InvalidTreeRoot: If the root is not an integer.
    :raises InvalidTreeFunctions: If either left_function or right_function is not callable.

    :return: The generated binary tree in dictionary form. If height is 0 or less, returns None.
    """

    if not isinstance(height, int):
        raise InvalidTreeHeight(height)
    if not isinstance(root, int):
        raise InvalidTreeRoot(root)
    if height <= 0:
        return None
        
    if not callable(left_function) or not callable(right_function):
        raise InvalidTreeFunctions(left_function, right_function)
    
    tree = {}
    stack = deque([(root, height, tree)])
    
    while stack:
        node, level, parent = stack.popleft()

        if level == 0:
            continue
        
        left_leaf:  int = left_function(node)
        right_leaf: int = right_function(node)
        
        parent[str(node)] = [
            {} if level > 1 else None,
            {} if level > 1 else None
        ]
        
        if level > 1:
            stack.append((left_leaf, level - 1, parent[str(node)][0]))
            stack.append((right_leaf, level - 1, parent[str(node)][1]))
        
    return tree


# print(gen_bin_tree_recursive(height_test))
# print(gen_bin_tree_iterative(height_test))
