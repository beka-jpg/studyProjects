import json


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = []

    def enroll(self, course_id):
        if course_id not in self.courses:
            self.courses.append(course_id)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "courses": self.courses
        }

    @staticmethod
    def from_dict(data):
        s = Student(data["student_id"], data["name"])
        s.courses = data.get("courses", [])
        return s

    def __str__(self):
        return f"{self.student_id} | {self.name} | Курсы: {self.courses}"


class Teacher:
    def __init__(self, teacher_id, name):
        self.teacher_id = teacher_id
        self.name = name

    def to_dict(self):
        return {
            "teacher_id": self.teacher_id,
            "name": self.name
        }

    @staticmethod
    def from_dict(data):
        return Teacher(data["teacher_id"], data["name"])

    def __str__(self):
        return f"{self.teacher_id} | {self.name}"


class Lesson:
    def __init__(self, lesson_id, title, content):
        self.lesson_id = lesson_id
        self.title = title
        self.content = content

    def to_dict(self):
        return {
            "lesson_id": self.lesson_id,
            "title": self.title,
            "content": self.content
        }

    @staticmethod
    def from_dict(data):
        return Lesson(data["lesson_id"], data["title"], data["content"])

    def __str__(self):
        return f"{self.lesson_id} | {self.title}"


class Course:
    def __init__(self, course_id, title, teacher_id):
        self.course_id = course_id
        self.title = title
        self.teacher_id = teacher_id
        self.lessons = []

    def add_lesson(self, lesson):
        for l in self.lessons:
            if l.lesson_id == lesson.lesson_id:
                print("❌ Урок уже существует")
                return
        self.lessons.append(lesson)
        print("📘 Урок добавлен")

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "title": self.title,
            "teacher_id": self.teacher_id,
            "lessons": [l.to_dict() for l in self.lessons]
        }

    @staticmethod
    def from_dict(data):
        c = Course(data["course_id"], data["title"], data["teacher_id"])
        c.lessons = [Lesson.from_dict(l) for l in data.get("lessons", [])]
        return c

    def __str__(self):
        return f"{self.course_id} | {self.title} | Учитель: {self.teacher_id}"


class EducationSystem:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.courses = []

    def find_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def find_teacher(self, teacher_id):
        for t in self.teachers:
            if t.teacher_id == teacher_id:
                return t
        return None

    def find_course(self, course_id):
        for c in self.courses:
            if c.course_id == course_id:
                return c
        return None

    def add_student(self, student):
        if self.find_student(student.student_id):
            print("❌ Студент уже существует")
            return
        self.students.append(student)
        print("🎓 Студент добавлен")

    def add_teacher(self, teacher):
        if self.find_teacher(teacher.teacher_id):
            print("❌ Преподаватель уже существует")
            return
        self.teachers.append(teacher)
        print("👨‍🏫 Преподаватель добавлен")

    def add_course(self, course):
        if self.find_course(course.course_id):
            print("❌ Курс уже существует")
            return
        if not self.find_teacher(course.teacher_id):
            print("❌ Преподаватель не найден")
            return
        self.courses.append(course)
        print("📚 Курс добавлен")

    def enroll_student(self, student_id, course_id):
        student = self.find_student(student_id)
        course = self.find_course(course_id)

        if not student or not course:
            print("❌ Студент или курс не найден")
            return

        student.enroll(course_id)
        print("✅ Студент записан на курс")

    def add_lesson_to_course(self, course_id, lesson):
        course = self.find_course(course_id)
        if not course:
            print("❌ Курс не найден")
            return
        course.add_lesson(lesson)

    def show_students(self):
        for s in self.students:
            print(s)

    def show_teachers(self):
        for t in self.teachers:
            print(t)

    def show_courses(self):
        for c in self.courses:
            print(c)

    def show_lessons(self, course_id):
        course = self.find_course(course_id)
        if not course:
            print("❌ Курс не найден")
            return

        if not course.lessons:
            print("Нет уроков")
            return

        for l in course.lessons:
            print(l)

    def to_dict(self):
        return {
            "students": [s.to_dict() for s in self.students],
            "teachers": [t.to_dict() for t in self.teachers],
            "courses": [c.to_dict() for c in self.courses]
        }

    def from_dict(self, data):
        self.students = [Student.from_dict(s) for s in data.get("students", [])]
        self.teachers = [Teacher.from_dict(t) for t in data.get("teachers", [])]
        self.courses = [Course.from_dict(c) for c in data.get("courses", [])]


class Storage:
    FILE_NAME = "education.json"

    @staticmethod
    def save(system):
        with open(Storage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(system.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(system):
        try:
            with open(Storage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                system.from_dict(data)
        except FileNotFoundError:
            print("📂 Новая система обучения")


def main():
    system = EducationSystem()
    Storage.load(system)

    while True:
        print("\n=== 🎓 ОНЛАЙН-КУРСЫ ===")
        print("1. Добавить студента")
        print("2. Добавить преподавателя")
        print("3. Добавить курс")
        print("4. Записать студента на курс")
        print("5. Добавить урок в курс")
        print("6. Показать студентов")
        print("7. Показать преподавателей")
        print("8. Показать курсы")
        print("9. Показать уроки курса")
        print("10. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            system.add_student(Student(input("ID: "), input("Имя: ")))

        elif choice == "2":
            system.add_teacher(Teacher(input("ID: "), input("Имя: ")))

        elif choice == "3":
            system.add_course(Course(
                input("ID курса: "),
                input("Название: "),
                input("ID преподавателя: ")
            ))

        elif choice == "4":
            system.enroll_student(
                input("ID студента: "),
                input("ID курса: ")
            )

        elif choice == "5":
            system.add_lesson_to_course(
                input("ID курса: "),
                Lesson(
                    input("ID урока: "),
                    input("Название урока: "),
                    input("Контент: ")
                )
            )

        elif choice == "6":
            system.show_students()

        elif choice == "7":
            system.show_teachers()

        elif choice == "8":
            system.show_courses()

        elif choice == "9":
            system.show_lessons(input("ID курса: "))

        elif choice == "10":
            Storage.save(system)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(system)
            print("👋 Выход")
            break

        else:
            print("❌ Неверный выбор")


if __name__ == "__main__":
    main()