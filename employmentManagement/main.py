import json


class Employee:
    def __init__(self, emp_id, name, position, salary, email):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.salary = salary
        self.email = email

    def raise_salary(self, amount):
        if amount <= 0:
            print("Сумма должна быть больше 0")
            return

        self.salary += amount
        print(f"Зарплата увеличена до {self.salary}")

    def change_position(self, new_position):
        self.position = new_position
        print(f"Должность изменена на {new_position}")

    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "position": self.position,
            "salary": self.salary,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        return Employee(
            data["emp_id"],
            data["name"],
            data["position"],
            data["salary"],
            data["email"]
        )

    def __str__(self):
        return f"{self.emp_id} | {self.name} | {self.position} | {self.salary} | {self.email}"


class Company:
    def __init__(self):
        self.employees = []

    def find_by_id(self, emp_id):
        for e in self.employees:
            if e.emp_id == emp_id:
                return e
        return None

    def find_by_email(self, email):
        for e in self.employees:
            if e.email.lower() == email.lower():
                return e
        return None

    def add_employee(self, employee):
        if self.find_by_id(employee.emp_id):
            print("❌ Сотрудник с таким ID уже существует")
            return

        if self.find_by_email(employee.email):
            print("❌ Email уже используется")
            return

        self.employees.append(employee)
        print("👤 Сотрудник добавлен")

    def show_employees(self):
        if not self.employees:
            print("Список пуст")
            return

        for i, e in enumerate(self.employees, 1):
            print(f"{i}. {e}")


    def update_employee(self, emp_id):
        emp = self.find_by_id(emp_id)
        if not emp:
            print("Сотрудник не найден")
            return

        print("1. Изменить имя")
        print("2. Изменить должность")
        print("3. Повысить зарплату")

        choice = input("Выбор: ")

        if choice == "1":
            emp.name = input("Новое имя: ")
            print("✅ Обновлено")

        elif choice == "2":
            emp.change_position(input("Новая должность: "))

        elif choice == "3":
            try:
                amount = float(input("Сумма: "))
                emp.raise_salary(amount)
            except ValueError:
                print("Ошибка ввода")

    def delete_employee(self, index):
        if 0 <= index < len(self.employees):
            removed = self.employees.pop(index)
            print(f"🗑 Удалён: {removed.name}")
        else:
            print("❌ Ошибка индекса")


    def search(self, keyword):
        results = [
            e for e in self.employees
            if keyword.lower() in e.name.lower() or keyword in e.emp_id
        ]

        if not results:
            print("Ничего не найдено")
            return

        for e in results:
            print(e)


    def to_dict(self):
        return [e.to_dict() for e in self.employees]

    def from_dict(self, data):
        self.employees = [Employee.from_dict(e) for e in data]


class Storage:
    FILE_NAME = "employees.json"

    @staticmethod
    def save(company):
        with open(Storage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(company.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(company):
        try:
            with open(Storage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                company.from_dict(data)
        except FileNotFoundError:
            print("📂 Новая база сотрудников")



def main():
    company = Company()
    Storage.load(company)

    while True:
        print("\n=== 🏢 СОТРУДНИКИ ===")
        print("1. Добавить сотрудника")
        print("2. Показать всех")
        print("3. Поиск")
        print("4. Изменить сотрудника")
        print("5. Удалить сотрудника")

        print("\n6. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            emp_id = input("ID: ")
            name = input("Имя: ")
            position = input("Должность: ")

            try:
                salary = float(input("Зарплата: "))
            except ValueError:
                print("Ошибка зарплаты")
                continue

            email = input("Email: ")

            company.add_employee(
                Employee(emp_id, name, position, salary, email)
            )

        elif choice == "2":
            company.show_employees()

        elif choice == "3":
            keyword = input("Поиск: ")
            company.search(keyword)

        elif choice == "4":
            emp_id = input("ID сотрудника: ")
            company.update_employee(emp_id)

        elif choice == "5":
            company.show_employees()
            try:
                index = int(input("Номер: ")) - 1
                company.delete_employee(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "6":
            Storage.save(company)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(company)
            print("👋 Выход + сохранение")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()