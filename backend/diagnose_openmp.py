#!/usr/bin/env python3
"""Diagnose OpenMP library conflicts in Python packages"""
import sys
import os
from pathlib import Path

print("=" * 80)
print("OpenMP LIBRARY CONFLICT DIAGNOSTIC")
print("=" * 80)

# Find all libomp.dylib files in the virtual environment
venv_path = Path(sys.prefix)
print(f"\nSearching in virtual environment: {venv_path}")

libomp_files = list(venv_path.rglob("libomp*.dylib"))

if not libomp_files:
    print("\n⚠️  No OpenMP libraries found in venv (checking site-packages)")
    site_packages = venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    libomp_files = list(site_packages.rglob("*omp*.dylib"))

print(f"\n{'='*80}")
print(f"Found {len(libomp_files)} OpenMP library files:")
print(f"{'='*80}\n")

for idx, lib_file in enumerate(libomp_files, 1):
    size = lib_file.stat().st_size
    package = lib_file.relative_to(venv_path)
    print(f"[{idx}] {lib_file.name}")
    print(f"    Size: {size:,} bytes")
    print(f"    Path: {package}")
    print(f"    Package: {str(package).split('/')[3] if len(str(package).split('/')) > 3 else 'unknown'}")
    print()

# Check which packages are likely culprits
print("=" * 80)
print("LIKELY CULPRIT PACKAGES:")
print("=" * 80)

packages_to_check = ['faiss-cpu', 'torch', 'numpy', 'scikit-learn', 'scipy']
import importlib.metadata

for pkg in packages_to_check:
    try:
        version = importlib.metadata.version(pkg)
        print(f"✓ {pkg}: {version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"✗ {pkg}: not installed")

print("\n" + "=" * 80)
print("SOLUTION: Set environment variable to use single OpenMP library")
print("=" * 80)
print("\nRecommendation:")
if libomp_files:
    homebrew_lib = [f for f in libomp_files if 'homebrew' in str(f)]
    if homebrew_lib:
        print(f"export DYLD_INSERT_LIBRARIES={homebrew_lib[0]}")
    else:
        print(f"export DYLD_INSERT_LIBRARIES={libomp_files[0]}")
else:
    print("Install OpenMP via Homebrew:")
    print("brew install libomp")
    print("export DYLD_INSERT_LIBRARIES=/opt/homebrew/opt/libomp/lib/libomp.dylib")
