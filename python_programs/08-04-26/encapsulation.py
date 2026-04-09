class Person:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


p = Person("A")
print(p.get_name())
p.set_name("B")
print(p.get_name())
