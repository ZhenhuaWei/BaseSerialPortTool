
'''
    the project needed chip, board and ip core object
'''
from collections import OrderedDict

class XObject():
    _objects = OrderedDict()
    _classes = None

    @classmethod
    def set_classes(cls, classes):
        cls._classes = classes

    @classmethod
    def get_classes(cls):
        return cls._classes

    @classmethod
    def create_object(cls, obj_name, class_name, *args, **kwargs):
        if class_name in cls._classes.keys(): 
            cls._objects[obj_name] = cls._classes[class_name](*args)
            return True;
        else:
            return False;
    
    @classmethod
    def get_object(cls, name, *args):
        if name in cls._objects.keys():
            return cls._objects[name]
        elif name in cls._classes.keys():
            return cls._classes[name](*args)
        else:
            return None

    @classmethod
    def set_object(cls, obj_name, obj):
        cls._objects[obj_name] = obj
        return True