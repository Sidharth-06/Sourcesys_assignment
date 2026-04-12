def make_multiplier(factor):
    def multiply(number):
        return number * factor

    return multiply


def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


if __name__ == "__main__":
    print("Closure example:")
    factor = get_integer("Enter a multiplier factor: ")
    number = get_integer("Enter a number to multiply: ")

    multiplier = make_multiplier(factor)
    print(multiplier(number))