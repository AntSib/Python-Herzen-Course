# Usage of singleton decorator
# By use of decorator, class will be converted to function, which is not assessible for OOP concepts
def singleton(cls: type) -> callable:
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


# Usage of metaclass as singleton
# By use of metaclass, class can be inherited from this metaclass, stayning as a class
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
