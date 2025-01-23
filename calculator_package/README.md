# README

## Description
Great package, which provides calculator framework.


## Common operations:

### Install from directory:

```shell
python -m pip install .
python -m pip install .[extra]
```

### Run installed package
```shell
python -m calculator
```

### Build
```shell
python -m pip install build
python -m build
```

### Install from tar archive
```shell
python -m pip install .
python -m pip install .[extra]
```

### Deploy package to test.pypi

```shell
python -m pip install twine
python -m twine upload --repository testpypi dist/*
python -m twine upload --repository testpypi dist/* --verbose
```

### Install from test pypi repository
```shell
python -m pip install calculator_framework-python_decoded --index-url https://test.pypi.org/simple/
python -m pip install calculator_framework-python_decoded==0.0.2 --index-url https://test.pypi.org/simple/
python -m pip install calculator_framework-python_decoded[extra]==0.0.2 --index-url https://test.pypi.org/simple/
```

### Uninstall package
```shell
python -m pip uninstall calculator_framework-python_decoded
```
