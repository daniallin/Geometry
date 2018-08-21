
class GeometryEntity():

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._args = tuple(args)
        obj._mhash = None  # will be set by __hash__ method.
        return obj

    def __str__(self):
        """Get the string of an object when use print(object)"""
        return type(self).__name__ + str(self.args)

    def __repr__(self):
        return type(self).__name__ + repr(self.args)

    @property
    def args(self):
        return self._args




