from setuptools import setup, find_packages

setup(
    name="decentralearn",
    version="2.1.2",
    packages=find_packages(),
    package_data={
        "decentralearn": ["Logo.jpg"],
    },
    include_package_data=True,
    install_requires=[
        "torch>=2.0.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "opacus>=1.1.0",
        "phe>=1.5.0",
        "web3>=6.0.0",
        "eth-tester>=0.9.0",
        "eth-utils>=2.1.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
        "dev": [
            "mypy>=1.0.0",
            "types-PyYAML>=6.0.0",
        ],
        "docs": [
            "sphinx>=4.5.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    python_requires=">=3.8",
    author="Jihad GARTI",
    author_email="jihad.garti2@gmail.com",
    description="A decentralized federated learning framework with privacy guarantees, created by Jihad GARTI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/decentralearn/decentralearn",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
) 