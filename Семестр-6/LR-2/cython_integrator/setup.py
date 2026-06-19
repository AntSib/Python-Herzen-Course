from Cython.Build import cythonize
from setuptools import setup

setup(
    # if file in root
    # ext_modules=cythonize(
    #     "integrate.pyx",
    #     compiler_directives={"language_level": "3"},
    # ),
    # if file in src
    ext_modules=cythonize(
        "src/integrate.pyx",
        compiler_directives={"language_level": "3"},
    ),
    package_dir={"": "src"},
)
