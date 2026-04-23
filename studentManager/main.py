import json


class Student:
    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.subjects = {}  # {subject: [grades]}

    def add_grade(self, subject, grade):
        if not (0 <= grade <= 100):
            print("Оценка должна быть от 0 до 100")
            return

        if subject not in self.subjects:
            self.subjects[subject] = []

        self.subjects[subject].append(grade)

    def average_by_subject(self, subject):
        grades = self.subjects.get(subject, [])
        return sum(grades) / len(grades) if grades else 0

    def overall_average(self):
        all_grades = []
        for grades in self.subjects.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def to_dict(self):
        return {
            "name": self.name,
            "group": self.group,
            "subjects": self.subjects
        }

   # загрузка из json файла.
    @staticmethod
    def from_dict(data):
        student = Student(data["name"], data["group"])
        student.subjects = data.get("subjects", {})
        return student

     # print
    def __str__(self):
        result = f"{self.name} | {self.group}\n"

        if not self.subjects:
            result += "  Нет оценок\n"
        else:
            for subject, grades in self.subjects.items():
                avg = self.average_by_subject(subject)
                result += f"  {subject}: {grades} (ср: {avg:.2f})\n"

        result += f"  Общий средний: {self.overall_average():.2f}"
        return result


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def show_students(self):
        if not self.students:
            print("Список пуст")
            return

        for i, student in enumerate(self.students, 1):
            print(f"\n{i}. {student}")

    def find_student(self, name):
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        return None

    def delete_student(self, index):
        if 0 <= index < len(self.students):
            self.students.pop(index)
        else:
            print("Неверный индекс")

    def save_to_file(self, filename="students.json"):
        data = [s.to_dict() for s in self.students]
        with open(filename, "w", encoding="utf-8") as f: # write
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename="students.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f: # read
                data = json.load(f)
                self.students = [Student.from_dict(s) for s in data]
        except FileNotFoundError:
            print("Файл не найден, начнём с пустого списка")


def main():
    manager = StudentManager()
    manager.load_from_file()

    while True:
        print("\n=== Система учёта студентов ===")
        print("1. Добавить студента")
        print("2. Показать всех")
        print("3. Добавить оценку по предмету")
        print("4. Найти студента")
        print("5. Удалить студента")
        print("6. Показать предметы студента")
        print("7. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            name = input("Имя: ")
            group = input("Группа: ")
            manager.add_student(Student(name, group))

        elif choice == "2":
            manager.show_students()

        elif choice == "3":
            name = input("Имя студента: ")
            student = manager.find_student(name)
            if student:
                subject = input("Предмет: ")
                try:
                    grade = int(input("Оценка: "))
                    student.add_grade(subject, grade)
                except ValueError:
                    print("Введите число")
            else:
                print("Студент не найден")

        elif choice == "4":
            name = input("Имя: ")
            student = manager.find_student(name)
            if student:
                print(student)
            else:
                print("Не найден")

        elif choice == "5":
            manager.show_students()
            try:
                index = int(input("Номер: ")) - 1
                manager.delete_student(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "6":
            name = input("Имя: ")
            student = manager.find_student(name)
            if student:
                if not student.subjects:
                    print("Нет предметов")
                else:
                    for subject, grades in student.subjects.items():
                        print(f"{subject}: {grades}")
            else:
                print("Не найден")

        elif choice == "7":
            manager.save_to_file()
            print("Сохранено")

        elif choice == "0":
            manager.save_to_file()
            print("Выход...")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()