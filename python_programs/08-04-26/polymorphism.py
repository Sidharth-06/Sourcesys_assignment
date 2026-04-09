

class Dog:
    def sound(self):
        return "Bark"


class Cat:
    def sound(self):
        return "Meow"


class Cow:
    def sound(self):
        return "Moo"


def print_sound(animal):
    print(animal.sound())


def main() -> int:
    animals = [Dog(), Cat(), Cow()]
    for animal in animals:
        print_sound(animal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
