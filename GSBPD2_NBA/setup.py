"""
Setup script for NBA SGP Engine package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Core dependencies
INSTALL_REQUIRES = [
    'pandas>=2.0.0',
    'numpy>=1.24.0',
    'scikit-learn>=1.3.0',
    'requests>=2.31.0',
    'nba_api>=1.1.0',  # NBA stats API
]

# Optional dependencies
EXTRAS_REQUIRE = {
    'ml': [
        'xgboost>=2.0.0',
        'lightgbm>=4.0.0',
    ],
    'api': [
        'requests>=2.31.0',
    ],
    'full': [
        'xgboost>=2.0.0',
        'lightgbm>=4.0.0',
        'requests>=2.31.0',
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0',
    ]
}

setup(
    name='nba-sgp-engine',
    version='1.0.0',
    author='NBA SGP Engine',
    description='Modular NBA Same Game Parlay prediction engine with ML models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/nba-sgp-engine',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.9',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    zip_safe=False,
)
