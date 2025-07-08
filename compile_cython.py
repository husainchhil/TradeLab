#!/usr/bin/env python3
"""
Generic compilation script for TradeLab Cython extensions.

Usage:
    python compile_cython.py           # Compile all .pyx files
    python compile_cython.py --clean   # Clean build artifacts
    python compile_cython.py --rebuild # Clean and rebuild all

This script handles:
- Automatic discovery of .pyx files
- Parallel compilation
- Cross-platform compatibility
- Development and production builds
"""

import os
import sys
import glob
import shutil
import argparse
import subprocess
from pathlib import Path


class CythonCompiler:
    """Generic Cython compiler for TradeLab."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.extensions_found = []

    def find_cython_files(self):
        """Find all .pyx files in the project."""
        pattern = str(self.project_root / "tradelab" / "**" / "*.pyx")
        pyx_files = glob.glob(pattern, recursive=True)

        self.extensions_found = []
        for pyx_file in pyx_files:
            rel_path = os.path.relpath(pyx_file, self.project_root)
            self.extensions_found.append(rel_path)

        return self.extensions_found

    def clean_build_artifacts(self):
        """Clean all build artifacts."""
        print("🧹 Cleaning build artifacts...")

        # Directories to clean
        dirs_to_clean = [
            self.build_dir,
            "dist",
            "*.egg-info",
        ]

        # File patterns to clean
        patterns_to_clean = [
            "**/*.c",  # Generated C files
            "**/*.html",  # Cython annotation files
            "**/*.so",  # Unix shared objects
            "**/*.pyd",  # Windows extensions
            "**/__pycache__",  # Python cache
        ]

        # Clean directories
        for dir_pattern in dirs_to_clean:
            for path in glob.glob(str(self.project_root / dir_pattern)):
                if os.path.isdir(path):
                    print(f"  Removing directory: {path}")
                    shutil.rmtree(path, ignore_errors=True)

        # Clean files
        for pattern in patterns_to_clean:
            for path in glob.glob(str(self.project_root / pattern), recursive=True):
                if os.path.isfile(path):
                    print(f"  Removing file: {path}")
                    os.remove(path)
                elif os.path.isdir(path):
                    print(f"  Removing directory: {path}")
                    shutil.rmtree(path, ignore_errors=True)

        print("✅ Clean complete!")

    def compile_extensions(self):
        """Compile all Cython extensions."""
        extensions = self.find_cython_files()

        if not extensions:
            print("❌ No .pyx files found!")
            return False

        print(f"🔨 Found {len(extensions)} Cython file(s):")
        for ext in extensions:
            print(f"  📄 {ext}")

        print("\n🚀 Starting compilation...")

        try:
            # Run the setup script
            cmd = [sys.executable, "setup.py", "build_ext", "--inplace"]
            result = subprocess.run(
                cmd, cwd=self.project_root, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Compilation successful!")
                print("\n📊 Generated files:")

                # Show generated files
                for pattern in ["**/*.so", "**/*.pyd", "**/*.c"]:
                    for path in glob.glob(str(self.project_root / "tradelab" / pattern), recursive=True):
                        rel_path = os.path.relpath(path, self.project_root)
                        print(f"  📦 {rel_path}")

                return True
            else:
                print("❌ Compilation failed!")
                print(f"Error: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return False

    def verify_installation(self):
        """Verify that compiled extensions can be imported."""
        print("\n🔍 Verifying compiled extensions...")

        # Try to import each extension
        success_count = 0
        for ext_path in self.extensions_found:
            # Convert path to module name
            module_name = ext_path.replace(os.sep, '.').replace('.pyx', '')

            try:
                __import__(module_name)
                print(f"  ✅ {module_name}")
                success_count += 1
            except ImportError as e:
                print(f"  ❌ {module_name}: {e}")

        if success_count == len(self.extensions_found):
            print("🎉 All extensions imported successfully!")
            return True
        else:
            print(
                f"⚠️  {success_count}/{len(self.extensions_found)} extensions working")
            return False


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Compile TradeLab Cython extensions")
    parser.add_argument("--clean", action="store_true",
                        help="Clean build artifacts")
    parser.add_argument("--rebuild", action="store_true",
                        help="Clean and rebuild")
    parser.add_argument("--verify", action="store_true",
                        help="Verify imports after compilation")

    args = parser.parse_args()

    compiler = CythonCompiler()

    if args.clean or args.rebuild:
        compiler.clean_build_artifacts()

    if not args.clean:  # If not just cleaning
        success = compiler.compile_extensions()

        if success and args.verify:
            compiler.verify_installation()


if __name__ == "__main__":
    main()
