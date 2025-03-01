import timeit
import matplotlib.pyplot as plt
from random import randint
from bin_tree.bin_tree import gen_bin_tree_recursive, gen_bin_tree_iterative
from bin_tree.bin_tree_exceptions import InvalidTreeHeight, InvalidTreeRoot
from bin_tree_complex_profiling import setup_plot

# simple timeit profiling
def main():
    max_height:     int = 16    # maximum height of tree to profile
    timeit_runs:    int = 100  # number of times to run each function
    functions_list: list = [gen_bin_tree_recursive, gen_bin_tree_iterative]
    times:          list = []   # list of execution times

    left_function = lambda x: x * 2 # use of default "left_function = lambda x: x ** 2"
                                    # may result in string overflow at relatively low height
    for func in functions_list:
        for height in range(1, max_height + 1):
            rand_root = randint(1, 100)
            exec_time = timeit.timeit(lambda: func(height, rand_root, left_function=left_function), number=timeit_runs)
            times.append(exec_time)
        plt.plot(times)
        times.clear()

    setup_plot(functions_list, label='Execution time with timeit', savefig=True)
    plt.show()

if __name__ == '__main__':
    main()
