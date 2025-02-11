import pytest
from bin_tree import gen_bin_tree_recursive
from bin_tree_exceptions import InvalidTreeHeight, InvalidTreeRoot, InvalidTreeFunctions

# for binary tree testing make class from Exception

class TestBinTree:
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

    def test_gen_bin_tree_empty_tree(self):
        tree = gen_bin_tree_recursive(0, 5, lambda x: x ** 2, lambda x: x - 2)
        assert tree is None

    def test_gen_bin_tree_negative_height(self):
        assert gen_bin_tree_recursive(-1, 5, lambda x: x ** 2, lambda x: x - 2) is None

    def test_gen_bin_tree_negative_root(self):
        assert isinstance(gen_bin_tree_recursive(6, -5, lambda x: x ** 2, lambda x: x - 2), dict)


if __name__ == "__main__":
    pytest.main()
