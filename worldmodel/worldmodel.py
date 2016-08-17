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

    def in_str(self):
        res_str = '<obj>\n'
        res_str += ('name = ' + self.name + '\n')
        if len(self.inclass) > 0:
            res_str += ('class = ')
            for ic in self.inclass:
                res_str += (ic.name + ';')
            res_str += ('\n')
        res_str += ('isclass = ')
        if self.isclass:
            res_str += ('True')
        else:
            res_str += ('False')
        res_str += ('\n')
        if len(self.informations) > 0:
            res_str += '<attr>\n'
            for ik in self.informations.keys():
                res_str += (str(ik) + ' = ' + str(self.informations[ik])
                            + '\n')
            res_str += '</attr>\n'
        res_str += ('</obj>\n')
        return res_str

    def from_str(self, in_lines, world):
        whichtag = ''
        for l in in_lines:
            sepe = l.split(' ')
            if '<attr>' in l:
                whichtag = 'attr'
                continue
            elif '</attr>' in l:
                whichtag = ''
                continue
            if whichtag == 'attr':
                att_sep = l.split(' ')
                self.informations[att_sep[0]] = ' '.join(att_sep[2:])
            elif sepe[0] == 'name' and len(sepe) >= 3:
                print('name:' + ' '.join(sepe[2:]))
                self.name = ' '.join(sepe[2:])
            elif sepe[0] == 'class':
                clss = sepe[2].split(';')
                for c in clss:
                    if len(c) > 0:
                        self.inclass.append(world.get_obj_by_name(c))
            elif sepe[0] == 'isclass':
                self.isclass = sepe[2] == 'True'


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
            print('class:', c.name, ' objs:', [
                  (x.name, x.informations) for x in objs])

    def get_obj_by_name(self, name):
        for o in self.objects:
            if o.name == name:
                return o

    def write_readable(self, filename):
        """
        Write file in readable format.
        """
        print('writing file.')
        try:
            file = open(filename, 'w', encoding='ascii')
            for o in self.objects:
                file.write(o.in_str())
            print(' [ done ]')
        except FileNotFoundError:
            print(' [ error ]')

    def read_readable(self, filename):
        """
        Read readable file in defined format.
        """
        print('opening from file.')
        objs = []
        try:
            file = open(filename, 'r')
            lines = file.read()
            lines = lines.split('\n')
            for l in lines[:]:
                if len(l) == 0:
                    lines.remove(l)
            isintag = False
            o_lines = []
            print(lines)
            for l in lines:
                if '<obj>' in l:
                    isintag = True
                elif '</obj>' in l:
                    isintag = False
                    new_o = Object()
                    new_o.from_str(o_lines, self)
                    objs.append(objs)
                    self.objects.append(new_o)
                    o_lines = []
                elif isintag:
                    o_lines.append(l)
            print(' [ done ]')
        except FileNotFoundError:
            print(' [ error ]')

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

    # wm.add_object(o_animal)
    # wm.add_object(o_car)
    # wm.add_object(o_cow)
    # wm.add_object(o_dog)
    # wm.add_object(o_cat)
    # wm.add_object(o_bmw)
    # wm.add_object(o_hyundai)
    # wm.add_object(o_toyota)
    # wm.print_objects()
    # wm.write_readable('data_test.xml')
    wm.read_readable('data_test.xml')
    wm.print_objects()
