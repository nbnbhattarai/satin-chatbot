import pickle
import re


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

    def from_str(self, in_lines):
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
                # print('name:' + ' '.join(sepe[2:]))
                self.name = ' '.join(sepe[2:])
            elif sepe[0] == 'class':
                clss = sepe[2].split(';')
                for c in clss:
                    if len(c) > 0:
                        self.inclass.append(c)
            elif sepe[0] == 'isclass':
                self.isclass = (sepe[2] == 'True')


class World:
    """
    This class represents the virtual representation
    of world. It is super class for all other classes and objects.
    It contains all the objects and their relationships.
    """

    def __init__(self):
        self.objects = {}       # objects in world
        self.classobjects = {}  # objects list with classname as key

    def add_object(self, obj):
        if obj.isclass:
            if obj.name not in self.classobjects.keys():
                self.classobjects[obj.name] = []
        if obj.name in self.objects.keys():
            print('Cannot add object, object with same name already exist')
        else:
            self.objects[obj.name] = obj
            for cl in obj.inclass:
                if cl in self.classobjects.keys():
                    if obj.name not in self.classobjects[cl]:
                        self.classobjects[cl] = self.classobjects[cl] +\
                            [obj.name]
                else:
                    self.classobjects[cl] = [obj.name]

    def print_objects(self):
        for c in self.classobjects.keys():
            print('class:', c, self.objects[c].informations)
        for o in self.objects.values():
            if not o.isclass:
                print('object:', o.name, o.informations)

    def write_readable(self, filename):
        """
        Write file in readable format.
        """
        print('writing file.')
        try:
            file = open(filename, 'w', encoding='ascii',
                        errors='surrogateescape')
            objects = self.objects.values()
            for o in objects:
                file.write(o.in_str())
            print(' [ done ]')
        except FileNotFoundError:
            print(' [ error ]')

    def read_readable(self, filename):
        """
        Read readable file in defined format.
        """
        print('opening worldmodel from file.' + filename, end='. ')
        try:
            file = open(filename, 'r',
                        errors='surrogateescape')
            text = file.read().replace('\n', '$')
            objects = re.findall(r'<obj>(.*?)</obj>', text)
            for o in objects:
                o_str = o.split('$')
                fr_str = []
                for os in o_str[:]:
                    fr_str.append(os.strip())
                temp_obj = Object()
                temp_obj.from_str(fr_str)
                self.add_object(temp_obj)
            print(' [ done ]')
        except FileNotFoundError:
            print(' [ error ]')

    def write(self, filename):
        """
        Write this clas to a file.
        """
        print('writing file.', end='')
        try:
            file = open(filename, 'wb')
            file.write(pickle.dumps(self.__dict__))
            print(' [ done ]')
        except FileNotFoundError:
            print(' [ error ]')

    def open_from_file(self, filename):
        print('opening from file.', end=',')
        try:
            file = open(filename, 'rb',
                        errors='surrogateescape')
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
    wm.read_readable('data.wm')
    wm.print_objects()
