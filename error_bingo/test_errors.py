import pytest


def test_type_error():

    with pytest.raises(TypeError):
        2 + "3"

    with pytest.raises(TypeError):
        sum([2, "3"])

    with pytest.raises(TypeError):
        2 > "3"

    with pytest.raises(TypeError):
        max(2, "3")

    with pytest.raises(TypeError):
        min(2, "3")

    with pytest.raises(TypeError):
        sorted([2, "3"])

    def func(a, b):
        ...

    with pytest.raises(TypeError):
        func(10)

    with pytest.raises(TypeError):
        func(10, 20, 30)

    with pytest.raises(TypeError):
        func(10, 20, foo=30)

    with pytest.raises(TypeError):
        a, b, c = 123

    with pytest.raises(TypeError):
        for i in 123:
            ...


def test_value_error():

    with pytest.raises(ValueError):
        int("FOOO")

    with pytest.raises(ValueError):
        open("foo", "invalid_mode")

    with pytest.raises(ValueError):
        a, b, c = [1, 2, 3, 4]


def test_lookup_errors():

    with pytest.raises(ModuleNotFoundError):
        import foo

    with pytest.raises(ImportError):
        from sys import foo

    with pytest.raises(NameError):
        foo

    with pytest.raises(AttributeError):
        list.foo

    with pytest.raises(KeyError):
        {}["fooo"]

    with pytest.raises(IndexError):
        [1, 2, 3][100000]

    with pytest.raises(LookupError):
       "abc".encode("FOOO")


def test_unicode_errors():

    with pytest.raises(UnicodeEncodeError):
        "Привіт".encode("ascii")

    data = "Привіт".encode()
    with pytest.raises(UnicodeDecodeError):
        data.decode("ascii")


def test_arithmetic_error():
    with pytest.raises(ZeroDivisionError):
        5 / 0

    with pytest.raises(OverflowError):
        1.23 ** 1000000000000000000000000000


    import numpy
    numpy.sqrt(-1)

    with pytest.raises(FloatingPointError):
        with numpy.errstate(invalid="raise"):
            numpy.sqrt(-1)


def test_function_errors():

    def func():
        func()

    with pytest.raises(RecursionError):
        func()

    def func():
        print(a)
        a = 123

    with pytest.raises(UnboundLocalError):
        func()


def iteration_errors():

    iterator = iter([])
    with pytest.raises(StopIteration):
        next(iterator)

    def gen():
        yield 1

    generator = gen()
    next(generator)
    with pytest.raises(StopIteration):
        next(generator)

    def gen():
        yield 1
        raise StopIteration

    generator = gen()
    next(generator)
    with pytest.raises(RuntimeError):
        next(generator)


def test_assertion_error():

    with pytest.raises(AssertionError):
        assert 1 > 10

    with pytest.raises(AssertionError):
        assert False

    with pytest.raises(AssertionError):
        assert None

    with pytest.raises(AssertionError):
        assert 0

    with pytest.raises(AssertionError):
        assert ""

    with pytest.raises(AssertionError):
        assert []

    with pytest.raises(AssertionError):
        assert {}

    with pytest.raises(AssertionError):
        assert range(0, 0)


def test_not_implemented_error():

    import numbers

    with pytest.raises(NotImplementedError):
        numbers.Real.__add__(1, 2)


@pytest.mark.skip("Manipulation with RAM")
def test_memory_error():
    a = [None]

    with pytest.raises(MemoryError):
        while True:
            a += a


def test_syntax_errors():

    with pytest.raises(SyntaxError):
        from error_bingo import syntax_error

    with pytest.raises(SyntaxError):
        eval("sdfj324o(*&")

    with pytest.raises(SyntaxError):
        exec("sdfj324o(*&")

    with pytest.raises(IndentationError):
        from error_bingo import indentation_error

    with pytest.raises(TabError):
        from error_bingo import tab_error


# todo
#  ReferenceError
#  SystemError
#  BufferError
#  EOFError
#  OSError
#       FileNotFoundError
#       FileExistsError
#       NotADirectoryError
#       ChildProcessError
#       BlockingIOError
#       TimeoutError
#       IOError
#       PermissionError
#       EnvironmentError
#       ProcessLookupError
#       IsADirectoryError
#       WindowsError
#       InterruptedError
#       ConnectionError
#            ConnectionRefusedError
#            BrokenPipeError
#            ConnectionResetError
#            ConnectionAbortedError
