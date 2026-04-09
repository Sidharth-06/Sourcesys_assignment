


class Student:
	def __init__(self, name, age):
		self.name = name
		self.age = age

	def show(self):
		print(f"Name: {self.name}")
		print(f"Age: {self.age}")


def main() -> int:
	student1 = Student("Asha", 20)
	student2 = Student("Ravi", 21)

	student1.show()
	
	student2.show()
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
