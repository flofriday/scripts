from setuptools import setup, find_packages

setup(
    name="scripts",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mkurl=mkurl.mkurl:main",
            "sourcepaper=sourcepaper.main:main",
        ],
    },
)
