from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lunatic-trader",
    version="2.0.0",
    author="Lunatic Trader Project",
    description="Lunar cycle trading strategy with comprehensive backtesting and statistical validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lunatic-trader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "yfinance>=0.2.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "crypto": ["python-binance", "cbpro"],
        "dev": ["pytest", "pytest-cov", "black", "flake8"],
    },
)
