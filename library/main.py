import json


class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.is_borrowed = False
        self.borrowed_by = None

    def borrow(self, user_name):
        if self.is_borrowed:
            print("Книга уже выдана")
            return False

        self.is_borrowed = True
        self.borrowed_by = user_name
        print(f"Книга выдана: {user_name}")
        return True

    def return_book(self):
        if not self.is_borrowed:
            print("Книга не была выдана")
            return False

        print(f"Книга возвращена от: {self.borrowed_by}")
        self.is_borrowed = False
        self.borrowed_by = None
        return True

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "is_borrowed": self.is_borrowed,
            "borrowed_by": self.borrowed_by
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["title"], data["author"], data["year"])
        book.is_borrowed = data.get("is_borrowed", False)
        book.borrowed_by = data.get("borrowed_by")
        return book

    def __str__(self):
        status = "Выдана" if self.is_borrowed else "В наличии"
        borrower = f" (у: {self.borrowed_by})" if self.borrowed_by else ""
        return f"{self.title} | {self.author} | {self.year} | {status}{borrower}"


class User:
    def __init__(self, name):
        self.name = name
        self.history = []

    def add_history(self, book_title):
        self.history.append(book_title)

    def __str__(self):
        return f"{self.name} | История: {self.history}"


class Library:
    def __init__(self):
        self.books = []
        self.users = []


    def find_user(self, name):
        for u in self.users:
            if u.name.lower() == name.lower():
                return u
        return None

    def create_user(self, name):
        if self.find_user(name):
            print("Пользователь уже существует")
            return

        self.users.append(User(name))
        print("👤 Пользователь создан")

    def show_users(self):
        if not self.users:
            print("Нет пользователей")
            return

        for i, u in enumerate(self.users, 1):
            print(f"{i}. {u}")

    def update_user(self, old_name, new_name):
        user = self.find_user(old_name)
        if not user:
            print("Пользователь не найден")
            return

        if self.find_user(new_name):
            print("Пользователь с таким именем уже существует")
            return

        user.name = new_name
        print("Пользователь обновлён")

    def delete_user(self, index):
        if 0 <= index < len(self.users):
            removed = self.users.pop(index)
            print(f"🗑 Удалён пользователь: {removed.name}")
        else:
            print("Ошибка индекса")


    def find_book(self, title):
        for b in self.books:
            if title.lower() in b.title.lower():
                return b
        return None

    def add_book(self, book):
        for b in self.books:
            if b.title.lower() == book.title.lower():
                print("Такая книга уже существует")
                return

        self.books.append(book)
        print("Книга добавлена")

    def show_books(self):
        if not self.books:
            print("Библиотека пуста")
            return

        for i, b in enumerate(self.books, 1):
            print(f"{i}. {b}")

    def delete_book(self, index):
        if 0 <= index < len(self.books):
            removed = self.books.pop(index)
            print(f"🗑 Удалена: {removed.title}")
        else:
            print("Ошибка индекса")


    def borrow_book(self, title, user_name):
        book = self.find_book(title)
        if not book:
            print("Книга не найдена")
            return

        user = self.find_user(user_name)
        if not user:
            print("Пользователь не найден (создайте его)")
            return

        if book.borrow(user.name):
            user.add_history(book.title)

    def return_book(self, title):
        book = self.find_book(title)
        if not book:
            print("Книга не найдена")
            return

        book.return_book()

    def to_dict(self):
        return {
            "books": [b.to_dict() for b in self.books],
            "users": [
                {
                    "name": u.name,
                    "history": u.history
                }
                for u in self.users
            ]
        }

    def from_dict(self, data):
        self.books = [Book.from_dict(b) for b in data.get("books", [])]

        self.users = []
        for u in data.get("users", []):
            user = User(u["name"])
            user.history = u.get("history", [])
            self.users.append(user)


class LibraryStorage:
    FILE_NAME = "library.json"

    @staticmethod
    def save(library):
        with open(LibraryStorage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(library.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(library):
        try:
            with open(LibraryStorage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                library.from_dict(data)
        except FileNotFoundError:
            print("📂 Новая библиотека создана")



def main():
    library = Library()
    LibraryStorage.load(library)

    while True:
        print("\n=== 📚 БИБЛИОТЕКА ===")
        print("1. Добавить книгу")
        print("2. Показать книги")
        print("3. Выдать книгу")
        print("4. Вернуть книгу")
        print("5. Удалить книгу")

        print("\n--- Пользователи ---")
        print("6. Создать пользователя")
        print("7. Показать пользователей")
        print("8. Изменить пользователя")
        print("9. Удалить пользователя")

        print("\n0. Сохранить и выйти")

        choice = input("Выбор: ")

        if choice == "1":
            title = input("Название: ")
            author = input("Автор: ")
            year = input("Год: ")
            library.add_book(Book(title, author, year))

        elif choice == "2":
            library.show_books()

        elif choice == "3":
            title = input("Книга: ")
            user = input("Пользователь: ")
            library.borrow_book(title, user)

        elif choice == "4":
            title = input("Книга: ")
            library.return_book(title)

        elif choice == "5":
            library.show_books()
            try:
                index = int(input("Номер: ")) - 1
                library.delete_book(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "6":
            name = input("Имя пользователя: ")
            library.create_user(name)

        elif choice == "7":
            library.show_users()

        elif choice == "8":
            old = input("Старое имя: ")
            new = input("Новое имя: ")
            library.update_user(old, new)

        elif choice == "9":
            library.show_users()
            try:
                index = int(input("Номер: ")) - 1
                library.delete_user(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "0":
            LibraryStorage.save(library)
            print("💾 Сохранено")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()