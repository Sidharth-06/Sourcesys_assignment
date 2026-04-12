class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


if __name__ == "__main__":
    print("Iterator example:")
    start_value = get_integer("Enter the starting number: ")

    for value in Countdown(start_value):
        print(value)