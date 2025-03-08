class Variant(type):
    """
    A metaclass that defines a variant that simulates as a constructor for a union type.
    """

    __union__: type

    def __instancecheck__(cls, instance):
        return isinstance(instance, cls.__union__) and cls.__instancecheck__(instance)
    
def variant(union):
    def decorator(cls):
        cls = Variant(cls.__name__, cls.__bases__, dict(cls.__dict__))
        cls.__union__ = union
        return cls
    return decorator
