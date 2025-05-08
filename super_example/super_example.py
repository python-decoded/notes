import inspect


class super:
    def __init__(self, _class=None, _object=None):

        if _class is None or _object is None:
            frame = inspect.currentframe()

            caller_frame = frame.f_back  # inspect 1 stack up
            first_arg_name = caller_frame.f_code.co_varnames[0]  # 1 param ('self' or 'cls')
            _object = caller_frame.f_locals[first_arg_name]
            _class = caller_frame.f_locals["__class__"]

        self._class = _class
        self._object = _object
        self._parent_class = _class.__mro__[1]

    def __getattr__(self, item):
        value = getattr(self._parent_class, item)
        if hasattr(value, "__get__"):
            return value.__get__(self._object, self._parent_class)
        return value


class A:
    def do(self):
        print("A")


class B(A):
    def do(self):
        super().do()
        print("B")


class C(B):
    def do(self):
        # super(C, self).do()
        super_obj = super(C, self)
        super_method = super_obj.do
        super_method()

        print("C")


C().do()
