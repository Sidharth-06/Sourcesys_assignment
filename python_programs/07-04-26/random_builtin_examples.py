"""Examples of Python's random module built-in functions."""

from __future__ import annotations

import random


def main() -> int:
    numbers = [10, 20, 30, 40, 50]
    names = ["Alice", "Bob", "Charlie", "Diana"]

    print("random() ->", random.random())
    print("randint(1, 100) ->", random.randint(1, 100))
    print("choice(names) ->", random.choice(names))
    print("sample(numbers, 3) ->", random.sample(numbers, 3))

    shuffled_numbers = numbers.copy()
    random.shuffle(shuffled_numbers)
    print("shuffle(numbers) ->", shuffled_numbers)

    print("uniform(1.5, 5.5) ->", random.uniform(1.5, 5.5))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
