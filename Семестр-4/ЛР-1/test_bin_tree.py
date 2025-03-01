import pytest
from bin_tree import gen_bin_tree_recursive, gen_bin_tree_iterative
from bin_tree_exceptions import InvalidTreeHeight, InvalidTreeRoot, InvalidTreeFunctions


class TestBinTreeRecursive:
    def test_gen_bin_tree(self):
        tree = gen_bin_tree_recursive(6, 5, lambda x: x ** 2, lambda x: x - 2)
        assert isinstance(tree, dict)
    
    def test_gen_bin_tree_invalid_height(self):
        with pytest.raises(InvalidTreeHeight):
            gen_bin_tree_recursive("6", 5, lambda x: x ** 2, lambda x: x - 2)
        
    def test_gen_bin_tree_invalid_root(self):
        with pytest.raises(InvalidTreeRoot):
            gen_bin_tree_recursive(6, "5", lambda x: x ** 2, lambda x: x - 2)

    def test_gen_bin_tree_invalid_functions(self):
        with pytest.raises(InvalidTreeFunctions):
            gen_bin_tree_recursive(6, 5, "lambda x: x ** 2", "lambda x: x - 2")
    
    def test_invalid_l_function_is_none(self):
        with pytest.raises(InvalidTreeFunctions):
            gen_bin_tree_recursive(3, 5, left_function=None, right_function=lambda x: x - 1)
    
    def test_invalid_r_function_is_none(self):
        with pytest.raises(InvalidTreeFunctions):
            gen_bin_tree_recursive(3, 5, left_function=lambda x: x + 1, right_function=None)

    def test_gen_bin_tree_empty_tree(self):
        tree = gen_bin_tree_recursive(0, 5, lambda x: x ** 2, lambda x: x - 2)
        assert tree is None

    def test_gen_bin_tree_negative_height(self):
        assert gen_bin_tree_recursive(-1, 5, lambda x: x ** 2, lambda x: x - 2) is None

    def test_gen_bin_tree_negative_root(self):
        assert isinstance(gen_bin_tree_recursive(6, -5, lambda x: x ** 2, lambda x: x - 2), dict)

    def test_custom_functions(self):
        tree = gen_bin_tree_recursive(2, 3, lambda x: x * 2, lambda x: x + 3)
        assert "3" in tree
        left, right = tree["3"]
        assert left == {"6": [None, None]}
        assert right == {"6": [None, None]}
    
    def test_tree_nested_depth(self):
        tree = gen_bin_tree_recursive(3, 5, lambda x: x ** 2, lambda x: x - 2)
        expected_tree = {
            "5": [
                {"25": [{"625": [None, None]}, {"23": [None, None]}]},
                {"3": [{"9": [None, None]}, {"1": [None, None]}]}
            ]
        }
        assert tree == expected_tree

class TestBinTreeIterative:
    def test_gen_bin_tree(self):
        tree = gen_bin_tree_iterative(6, 5, lambda x: x ** 2, lambda x: x - 2)
        assert isinstance(tree, dict)
    
    def test_gen_bin_tree_invalid_height(self):
        with pytest.raises(InvalidTreeHeight):
            gen_bin_tree_iterative("6", 5, lambda x: x ** 2, lambda x: x - 2)
        
    def test_gen_bin_tree_invalid_root(self):
        with pytest.raises(InvalidTreeRoot):
            gen_bin_tree_iterative(6, "5", lambda x: x ** 2, lambda x: x - 2)

    def test_gen_bin_tree_invalid_functions(self):
        with pytest.raises(InvalidTreeFunctions):
            gen_bin_tree_iterative(6, 5, "lambda x: x ** 2", "lambda x: x - 2")
    
    def test_invalid_l_function_is_none(self):
        with pytest.raises(InvalidTreeFunctions):
            gen_bin_tree_iterative(3, 5, left_function=None, right_function=lambda x: x - 1)
    
    def test_invalid_r_function_is_none(self):
        with pytest.raises(InvalidTreeFunctions):
            gen_bin_tree_iterative(3, 5, left_function=lambda x: x + 1, right_function=None)

    def test_gen_bin_tree_empty_tree(self):
        tree = gen_bin_tree_iterative(0, 5, lambda x: x ** 2, lambda x: x - 2)
        assert tree is None

    def test_gen_bin_tree_negative_height(self):
        assert gen_bin_tree_iterative(-1, 5, lambda x: x ** 2, lambda x: x - 2) is None

    def test_gen_bin_tree_negative_root(self):
        assert isinstance(gen_bin_tree_iterative(6, -5, lambda x: x ** 2, lambda x: x - 2), dict)

    def test_custom_functions(self):
        tree = gen_bin_tree_iterative(2, 3, lambda x: x * 2, lambda x: x + 3)
        assert "3" in tree
        left, right = tree["3"]
        assert left == {"6": [None, None]}
        assert right == {"6": [None, None]}
    
    def test_tree_nested_depth(self):
        tree = gen_bin_tree_iterative(3, 5, lambda x: x ** 2, lambda x: x - 2)
        expected_tree = {
            "5": [
                {"25": [{"625": [None, None]}, {"23": [None, None]}]},
                {"3": [{"9": [None, None]}, {"1": [None, None]}]}
            ]
        }
        assert tree == expected_tree


if __name__ == "__main__":
    pytest.main()
