"""Simple try/except error handling examples in Python."""

from __future__ import annotations


def safe_divide(left: float, right: float) -> float | None:
    try:
        return left / right
    except ZeroDivisionError:
        print("Cannot divide by zero.")
        return None


def parse_age(text: str) -> int | None:
    try:
        age = int(text)
        if age < 0:
            raise ValueError("age cannot be negative")
        return age
    except ValueError as error:
        print(f"Invalid age: {error}")
        return None


def main() -> int:
    print("Division example:")
    result = safe_divide(10, 0)
    print("Result:", result)

    print("\nInput validation example:")
    age = parse_age("twenty")
    print("Parsed age:", age)

    print("\nList access example:")
    items = ["apple", "banana"]
    try:
        print(items[5])
    except IndexError:
        print("That list index does not exist.")
    finally:
        print("Finished error handling demo.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
