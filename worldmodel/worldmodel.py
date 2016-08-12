import pickle

class Object:
    """
    This class represents the object's model of
    the world.
    """
    def __init__(self, obj_name=None, obj_class=None, isclass=False,
                 class_name=None):
        self.inclass = []       # can be in multiple class..
        self.isclass = isclass
        if class_name:
            self.class_name = class_name
        if obj_name:
            self.name = obj_name
        if obj_class:
            self.inclass.append(obj_class)
        self.informations = {}  # store object's informations..


class World:
    """
    This class represents the virtual representation
    of world.
    """
    def __init__(self):
        self.objects = []       # objects in world

    def add_object(obj, self):
        self.objects.append(obj)

    def get_obj_of_class(self, o_class):
        res = []
        for o in self.objects:
            if o_class in o.inclass:
                res.apppend(o)
        return res

    def write(self, filename):
        """
        Write this clas to a file.
        """
        print('writing file.')
        try:
            file = open(filename, 'wb')
            file.write(pickle.dumps(self.__dict__))
            print(' [ done ]')
        except FileNotFoundError:
            print(' [ error ]')

    def open_from_file(self, filename):
        print('opening from file.')
        try:
            file = open(filename, 'rb')
            datapickle = file.read()
            file.close()
            self.__dict__ = pickle.loads(datapickle)
            print(' [ done ]')
        except FileNotFoundError:
            print(' [ error ]')

    
