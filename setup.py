"""Setup script for building TradeLab with Cython extensions."""

import os
import numpy
from setuptools import setup, find_packages
from Cython.Build import cythonize
from setuptools.extension import Extension

# Find all .pyx files recursively


def find_pyx_files():
    pyx_files = []
    for root, dirs, files in os.walk("tradelab"):
        for file in files:
            if file.endswith(".pyx"):
                pyx_path = os.path.join(root, file)
                # Convert file path to module name
                module_name = pyx_path.replace(os.sep, ".").replace(".pyx", "")
                pyx_files.append((module_name, pyx_path))
    return pyx_files

# Create extensions from .pyx files


def create_extensions():
    pyx_files = find_pyx_files()
    extensions = []

    for module_name, pyx_path in pyx_files:
        ext = Extension(
            module_name,
            [pyx_path],
            include_dirs=[numpy.get_include()],
            define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        )
        extensions.append(ext)

    return extensions


# Get extensions
extensions = create_extensions()

# Print found extensions for debugging
print(f"Found {len(extensions)} Cython extensions:")
for ext in extensions:
    print(f"  - {ext.name}")

# Setup configuration
setup(
    packages=find_packages(),
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
        }
    ),
    zip_safe=False,
    include_package_data=True,
)
