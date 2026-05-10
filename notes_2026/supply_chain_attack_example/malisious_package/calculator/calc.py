from numbers import Complex


class Calc:

    OPERATIONS = {"add": lambda a, b: a + b,
                  "sub": lambda a, b: a - b,
                  "mul": lambda a, b: a * b,
                  "div": lambda a, b: a / b}

    @classmethod
    def calculate(cls, a: Complex, b: Complex,
                  operation: str = "add",
                  key: callable = None):

        print(f"Calculate: {a} and {b}, "
              f"operation: {operation if not key else key.__name__}")

        assert isinstance(a, Complex)
        assert isinstance(b, Complex)

        func = key if key is not None else cls.OPERATIONS[operation]
        res = func(a, b)

        print(f"Result: {res}")

        return res

    @classmethod
    def run(cls):

        while True:
            msg = input("operation, a, b: ")
            operation, a, b = map(str.strip, msg.split(","))
            a = complex(a) if "j" in a else float(a)
            b = complex(b) if "j" in b else float(b)
            cls.calculate(a, b, operation)
            print("======================================")

    @classmethod
    def register(cls, name: str):

        def add_to_registry(func: callable):

            assert name not in cls.OPERATIONS
            cls.OPERATIONS[name] = func
            return func

        return add_to_registry
