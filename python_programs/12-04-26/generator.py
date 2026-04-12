def read_non_empty_lines(lines):
    for line in lines:
        cleaned = line.strip()
        if cleaned:
            yield cleaned


def get_items(prompt):
    raw_text = input(prompt)
    return raw_text.split(",")


if __name__ == "__main__":
    print("Generator example:")
    items = get_items("Enter values: ")

    for item in read_non_empty_lines(items):
        print(item)