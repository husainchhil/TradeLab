"""
Generic setup script for compiling Cython extensions in TradeLab.

This script automatically discovers and compiles all .pyx files in the package.
Add new Cython modules by simply placing .pyx files in the appropriate directories.
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os
import glob


def find_cython_extensions():
    """
    Automatically discover all .pyx files in the package and create Extension objects.

    Returns:
        List of Extension objects for all found .pyx files
    """
    extensions = []

    # Find all .pyx files recursively
    pyx_files = glob.glob("tradelab/**/*.pyx", recursive=True)

    for pyx_file in pyx_files:
        # Convert file path to module name
        # e.g., "tradelab/indicators/trend/ema/ema.pyx" -> "tradelab.indicators.trend.ema.ema"
        module_path = pyx_file.replace(os.sep, '.').replace('.pyx', '')

        # Create extension
        ext = Extension(
            name=module_path,
            sources=[pyx_file],
            include_dirs=[np.get_include()],
            define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
            extra_compile_args=[
                "-O3", "-ffast-math"] if os.name != 'nt' else ["/O2"],
            language="c"
        )

        extensions.append(ext)
        print(f"Found Cython module: {module_path}")

    return extensions


def main():
    """Main compilation function."""
    print("Discovering Cython extensions...")
    extensions = find_cython_extensions()

    if not extensions:
        print("No .pyx files found. Nothing to compile.")
        return

    print(f"Compiling {len(extensions)} Cython extension(s)...")

    setup(
        name="tradelab-cython-extensions",
        ext_modules=cythonize(
            extensions,
            compiler_directives={
                'language_level': 3,
                'boundscheck': False,
                'wraparound': False,
                'initializedcheck': False,
                'cdivision': True,
                'embedsignature': True,
                'annotation_typing': True,
            },
            annotate=True,  # Generate HTML annotation files for debugging
        ),
        zip_safe=False,
    )

    print("Compilation complete!")


if __name__ == "__main__":
    main()
