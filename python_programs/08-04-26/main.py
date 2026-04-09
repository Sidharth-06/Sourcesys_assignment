


def add_numbers(first, second):
	return first + second


def greet(name):
	return f"Hello, {name}!"


def display_result():
	total = add_numbers(10, 15)
	print("Total:", total)
	print(greet("Student"))


def main() -> int:
	display_result()
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
