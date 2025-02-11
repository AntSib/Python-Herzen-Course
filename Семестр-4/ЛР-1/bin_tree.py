from bin_tree_exceptions import InvalidTreeHeight, InvalidTreeRoot, InvalidTreeFunctions

# parameters
height: int = 6
root: int = 5
left_leaf_function = lambda x: x ** 2
right_leaf_function = lambda x: x - 2

# for debugging with prints
height_test: int = 2


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
