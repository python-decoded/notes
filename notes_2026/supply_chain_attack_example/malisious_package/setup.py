import setuptools


with open("README.md", "r") as file:
    long_description = file.read()


setuptools.setup(
    name="calculator_framework",
    version="0.0.1",
    author="Python Decoded",
    author_email="author@example.com",
    description="A simple arithmetic package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/calculator_framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],

    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "mypy", "tzdata; sys_platform == 'win32'"
    ],
    extras_require={"extra": ["pytest", "flake8"]}
)
