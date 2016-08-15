import pickle


class Object:
    """
    This class represents the object's model of
    the world.
    """

    def __init__(self, name=None, objclass=None, isclass=False):
        self.inclass = []       # can be in multiple class..
        self.isclass = isclass

        if name:
            self.name = name
        if objclass:
            self.inclass.append(objclass)

        # Store informations in the dictionary with specific value to
        # a specific attribute
        self.informations = {}


class World:
    """
    This class represents the virtual representation
    of world. It is super class for all other classes and objects.
    It contains all the objects and their relationships.
    """

    def __init__(self):
        self.objects = []       # objects in world

    def add_object(self, obj):
        self.objects.append(obj)

    def get_obj_of_class(self, o_class):
        res = []
        for o in self.objects:
            if o_class in o.inclass:
                res.append(o)
        return res

    def print_objects(self):
        classes_list = []
        for o in self.objects:
            if o.isclass:
                classes_list.append(o)

        for c in classes_list:
            objs = self.get_obj_of_class(c)
            print('class:', c.name, ' objs:', [(x.name, x.informations) for x in objs])

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

if __name__ == '__main__':
    wm = World()
    o_animal = Object(name='animal', isclass=True)
    o_car = Object(name='car', isclass=True)
    o_cow = Object(name='cow', isclass=True, objclass=o_animal)
    o_dog = Object(name='dog', isclass=True, objclass=o_animal)
    o_cat = Object(name='cat', isclass=True, objclass=o_animal)
    o_bmw = Object(name='bmw', isclass=True, objclass=o_car)
    o_hyundai = Object(name='hyundai', isclass=True, objclass=o_car)
    o_toyota = Object(name='toyota', isclass=True, objclass=o_car)

    o_cow.informations['horn'] = 2
    o_dog.informations['horn'] = False
    o_cat.informations['horn'] = False

    o_bmw.informations['wheel'] = 4
    o_hyundai.informations['wheel'] = 6
    o_toyota.informations['wheel'] = 8

    wm.add_object(o_animal)
    wm.add_object(o_car)
    wm.add_object(o_cow)
    wm.add_object(o_dog)
    wm.add_object(o_cat)
    wm.add_object(o_bmw)
    wm.add_object(o_hyundai)
    wm.add_object(o_toyota)
    wm.print_objects()
