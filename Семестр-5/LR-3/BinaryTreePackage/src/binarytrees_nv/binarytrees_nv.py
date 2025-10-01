from collections import deque

from .exceptions import (
    InvalidTreeFunctions,
    InvalidTreeHeight,
    InvalidTreeRoot,
)


def leaf_function(x):
    """Example function to generate the left/right leaf of a binary tree given a node."""
    return x**2


def gen_bin_tree_recursive(
    height: int,
    root: int = 1,
    left_function=lambda x: x,
    right_function=lambda x: x,
):
    """
    Generates a binary tree recursively given a height and a root node.

    Args:
        height (int): The height of the tree.
        root (int): The root node of the tree.
        left_function (callable): The function to generate the left leaf of the tree. Default is lambda x: x.
        right_function (callable): The function to generate the right leaf of the tree. Default is lambda x: x.

    Raises:
        InvalidTreeHeight: If the height is not an integer.
        InvalidTreeRoot: If the root is not an integer.
        InvalidTreeFunctions: If either left_function or right_function is not callable.

    Returns:
        The generated binary tree. If height is 0 or less, returns None.

    """
    if not isinstance(height, int):
        raise InvalidTreeHeight(height)  # Custom exception
    if not isinstance(root, int):
        raise InvalidTreeRoot(root)  # Custom exception

    if height <= 0:
        return None

    if not callable(left_function) or not callable(right_function):
        raise InvalidTreeFunctions(left_function, right_function)  # Custom exception

    left_leaf: int = left_function(root)
    right_leaf: int = right_function(root)

    return {
        str(root): [
            gen_bin_tree_recursive(
                height - 1,
                left_leaf,
                left_function,
                right_function,
            ),
            gen_bin_tree_recursive(
                height - 1,
                right_leaf,
                left_function,
                right_function,
            ),
        ],
    }


def gen_bin_tree_iterative(
    height: int,
    root: int = 1,
    left_function=lambda x: x,
    right_function=lambda x: x,
):
    """
    Generates a binary tree iteratively given a height and a root node.

    Args:
        height (int): The height of the tree. Must be a non-negative integer.
        root (int): The root node of the tree. Must be an integer.
        left_function (callable): The function to generate the left leaf of the tree. Default is lambda x: x.
        right_function (callable): The function to generate the right leaf of the tree. Default is lambda x: x.

    Raises:
        InvalidTreeHeight: If the height is not an integer.
        InvalidTreeRoot: If the root is not an integer.
        InvalidTreeFunctions: If either left_function or right_function is not callable.

    Returns:
        The generated binary tree in dictionary form. If height is 0 or less, returns None.

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

        left_leaf: int = left_function(node)
        right_leaf: int = right_function(node)

        parent[str(node)] = [{} if level > 1 else None, {} if level > 1 else None]

        if level > 1:
            stack.append((left_leaf, level - 1, parent[str(node)][0]))
            stack.append((right_leaf, level - 1, parent[str(node)][1]))

    return tree
