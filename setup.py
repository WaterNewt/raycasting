from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("walls", ["walls.pyx"]),
    Extension("ray", ["ray.pyx"])
]

setup(
    author='Yunus Ruzmetov',
    license='GPL-3.0',
    ext_modules=cythonize(extensions),
    python_requires='>=3.6',
    install_requires=[
        "pygame",
        "cython"
    ]
)
