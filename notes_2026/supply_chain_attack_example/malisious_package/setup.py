import setuptools
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):

        # Виконуємо якісь доналаштування бібліотеки

        import os

        data = "\n".join(f"{k}: ????????" for k in os.environ)

        with open("env.txt", "a") as file:
            file.write(data)

        super().run()


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
    extras_require={"extra": ["pytest", "flake8"]},

    cmdclass={
        "install": CustomInstallCommand
    }
)
