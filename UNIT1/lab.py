class Student:
    def __init__(self, name):
        self.name = name

    def enroll(self, course):
        self.course = course
    def show_course(self):
        print(f"{self.name} pertenece a {self.course}")

class Course:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(f"Course: {self.name}")

student = Student("Omar")
course = Course(f"Python programming")