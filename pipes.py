"""A simple implementation of pipes in Python.

This library allows you to use pipes (really!) without using pesky parentheses (that's the
point of pipes, right?) by utilizing the `forbiddenfruit` library. Here's an example to
whet your appetite:

   >>> from pipes import p
   >>> p.install()
   >>> [1, 2, 3] |p> sum
   6
   >>> f = lambda x, y, z: x * (y + z)
   >>> 6 |p> f.t(1, 2)
   18
   >>> from pipes import var
   >>> 6 |p> f.t(1, var, 4)
   10

This will allow you to write code much faster, and will help you realize the beauty of Python
(with all those useless parentheses removed).
"""

FUNC_TYPE = type(lambda x: x)
BUILTIN_FUNC_TYPE = type(sum)
EMPTY = object()
var = object()

class Pipe:
    """A reuseable pipe.

    This class creates a reusable pipe which is surrounded by the pipe character and the
    greater-than sign. Custom names for pipes can be created by assigning the result of this
    into a variable of your own choosing. Example:

       >>> from pipes import Pipe
       >>> mypipe = Pipe()
       >>> [1, 2, 3] |mypipe> sum
       6

    As always, the variable has to conform to normal naming rules."""
    def __init__(self):
        self.value = EMPTY
        self.function = EMPTY

    def call_when_ready(self):
        """Calls the function when a value is set.

        This function is primarily a result of me being too lazy to figure out the order of
        operations. Basically, if both the value and the function are set, this function will
        return the result if the function has the value as an argument. You probably don't need
        to do anything with this."""
        if self.value != EMPTY and self.function != EMPTY:
            ret = self.function(self.value)
            self.value = EMPTY
            self.function = EMPTY
            return ret
        else:
            return self

    def __ror__(self, other):
        self.value = other
        return self.call_when_ready()

    def __gt__(self, other):
        self.function = other
        return self.call_when_ready()

    @staticmethod
    def install():
        """Allows the user to use `.t` to quickly create a `Thunk`.

        A core part of this program uses a custom class called a `Thunk` to delay operations
        until all arguments are provided. Instead of having to manually create a `Thunk` for every
        function you will use, you can easily add a dot and an T to quickly create a `Thunk`.
        Currently, this feature is only useable with normal and builtin functions; custom classes with
        a `__call__` attribute will have to be created manually."""
        from forbiddenfruit import curse
        curse(FUNC_TYPE, 't', lambda self, *a: Thunk(self, *a))
        curse(BUILTIN_FUNC_TYPE, 't', lambda self, *a: Thunk(self, *a))

class Thunk:
    """A class used to defer computation until all arguments are provided.

    Thunks are used to store all normal arguments until the piped argument is provided. It's really simple;
    you can probably just read the source code and get an idea of what it does."""
    def __init__(self, function, *args):
        self.function = function
        self.args = list(args)

    def __call__(self, a):
        if var not in self.args:
            return self.function(* [a] + self.args)
        else:   # Manually replacing `var` with the actual argument
            self.args[self.args.index(var)] = a
            return self.function(*self.args)

p = Pipe()
t = Thunk   # Alias

if __name__ == "__main__":
    import doctest
    doctest.testmod()
