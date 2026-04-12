from functools import wraps
from time import perf_counter


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result

    return wrapper


@timer
def total_numbers(limit):
    return sum(range(limit))


def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


if __name__ == "__main__":
    print("Decorator example:")
    limit = get_integer("Enter a number to sum up to: ")
    print(total_numbers(limit))