import json


class Contact:
    def __init__(self, name, phone, email=None):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        return Contact(
            data["name"],
            data["phone"],
            data.get("email") # nullable
        )

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email or '-'}"


class ContactManager:
    def __init__(self):
        self.contacts = []


    def is_duplicate(self, name, phone):
        for c in self.contacts:
            if c.name.lower() == name.lower() or c.phone == phone:
                return True
        return False
    def add_contact(self, contact):
        if self.is_duplicate(contact.name, contact.phone):
            print("Такой контакт уже существует (имя или номер повторяются)")
            return

        self.contacts.append(contact)
        print("Контакт добавлен")

    def show_all(self):
        if not self.contacts:
            print("Список пуст")
            return

        for i, c in enumerate(self.contacts, 1):
            print(f"{i}. {c}")

    def find_contact(self, name):
        for c in self.contacts:
            if c.name.lower() == name.lower():
                return c
        return None

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            removed = self.contacts.pop(index)
            print(f"Удалён: {removed.name}")
        else:
            print("Неверный индекс")

    def search(self, keyword):
        results = [
            c for c in self.contacts
            if keyword.lower() in c.name.lower() or keyword in c.phone
        ]

        if not results:
            print("Ничего не найдено")
            return

        for r in results:
            print(r)

    def to_dict(self):
        return [c.to_dict() for c in self.contacts]

    def from_dict(self, data):
        self.contacts = [Contact.from_dict(c) for c in data]


class ContactStorage:
    FILE_NAME = "contacts.json"

    @staticmethod
    def save(manager):
        with open(ContactStorage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(manager.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(manager):
        try:
            with open(ContactStorage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                manager.from_dict(data)
        except FileNotFoundError:
            print("Файл не найден, создаём новую книгу")


def main():
    manager = ContactManager()
    ContactStorage.load(manager)

    while True:
        print("\n=== 📱 ТЕЛЕФОННАЯ КНИГА ===")
        print("1. Добавить контакт")
        print("2. Показать все")
        print("3. Поиск")
        print("4. Удалить контакт")
        print("5. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            name = input("Имя: ")
            phone = input("Телефон: ")
            email = input("Email (необязательно): ")
            manager.add_contact(Contact(name, phone, email))

        elif choice == "2":
            manager.show_all()

        elif choice == "3":
            keyword = input("Введите имя или номер: ")
            manager.search(keyword)

        elif choice == "4":
            manager.show_all()
            try:
                index = int(input("Номер для удаления: ")) - 1
                manager.delete_contact(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "5":
            ContactStorage.save(manager)
            print("Сохранено")

        elif choice == "0":
            ContactStorage.save(manager)
            print("Выход + сохранение")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()