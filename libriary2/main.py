import json



class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrowed_by = None

    def borrow(self, user_name):
        if self.is_borrowed:
            return False

        self.is_borrowed = True
        self.borrowed_by = user_name
        return True

    def return_book(self):
        if not self.is_borrowed:
            return False

        self.is_borrowed = False
        self.borrowed_by = None
        return True

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "is_borrowed": self.is_borrowed,
            "borrowed_by": self.borrowed_by
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["book_id"], data["title"], data["author"])
        book.is_borrowed = data.get("is_borrowed", False)
        book.borrowed_by = data.get("borrowed_by")
        return book

    def __str__(self):
        status = "📕 ВЫДАНА" if self.is_borrowed else "📗 В наличии"
        return f"{self.book_id} | {self.title} | {self.author} | {status}"



class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.history = []

    def add_history(self, book_title):
        self.history.append(book_title)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "history": self.history
        }

    @staticmethod
    def from_dict(data):
        user = User(data["user_id"], data["name"])
        user.history = data.get("history", [])
        return user

    def __str__(self):
        return f"{self.user_id} | {self.name}"



class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def find_book(self, book_id):
        for b in self.books:
            if b.book_id == book_id:
                return b
        return None

    def find_user(self, user_id):
        for u in self.users:
            if u.user_id == user_id:
                return u
        return None


    def add_book(self, book):
        if self.find_book(book.book_id):
            print("Книга уже существует")
            return

        self.books.append(book)
        print("📚 Книга добавлена")

    def add_user(self, user):
        if self.find_user(user.user_id):
            print("Пользователь уже существует")
            return

        self.users.append(user)
        print("👤 Пользователь добавлен")


    def show_books(self):
        if not self.books:
            print("Библиотека пуста")
            return

        for b in self.books:
            print(b)

    def show_users(self):
        if not self.users:
            print("Нет пользователей")
            return

        for u in self.users:
            print(u)


    def borrow_book(self, book_id, user_id):
        book = self.find_book(book_id)
        user = self.find_user(user_id)

        if not book:
            print("❌ Книга не найдена")
            return

        if not user:
            print("Пользователь не найден")
            return

        if book.borrow(user.name):
            user.add_history(book.title)
            print("Книга выдана")
        else:
            print("Книга уже занята")


    def return_book(self, book_id):
        book = self.find_book(book_id)

        if not book:
            print("Книга не найдена")
            return

        if book.return_book():
            print("📗 Книга возвращена")
        else:
            print("❌ Книга не была выдана")


    def show_user_history(self, user_id):
        user = self.find_user(user_id)

        if not user:
            print("Пользователь не найден")
            return

        print(f"\nИстория {user.name}:")
        if not user.history:
            print("Пусто")
        else:
            for h in user.history:
                print(" -", h)


    def to_dict(self):
        return {
            "books": [b.to_dict() for b in self.books],
            "users": [u.to_dict() for u in self.users]
        }

    def from_dict(self, data):
        self.books = [Book.from_dict(b) for b in data.get("books", [])]
        self.users = [User.from_dict(u) for u in data.get("users", [])]


class Storage:
    FILE_NAME = "library.json"

    @staticmethod
    def save(lib):
        with open(Storage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(lib.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(lib):
        try:
            with open(Storage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                lib.from_dict(data)
        except FileNotFoundError:
            print("📂 Новая библиотека")


def main():
    lib = Library()
    Storage.load(lib)

    while True:
        print("\n=== 📚 БИБЛИОТЕКА ===")
        print("1. Добавить книгу")
        print("2. Добавить пользователя")
        print("3. Показать книги")
        print("4. Показать пользователей")
        print("5. Выдать книгу")
        print("6. Вернуть книгу")
        print("7. История пользователя")

        print("\n8. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            bid = input("ID книги: ")
            title = input("Название: ")
            author = input("Автор: ")
            lib.add_book(Book(bid, title, author))

        elif choice == "2":
            uid = input("ID пользователя: ")
            name = input("Имя: ")
            lib.add_user(User(uid, name))

        elif choice == "3":
            lib.show_books()

        elif choice == "4":
            lib.show_users()

        elif choice == "5":
            bid = input("ID книги: ")
            uid = input("ID пользователя: ")
            lib.borrow_book(bid, uid)

        elif choice == "6":
            bid = input("ID книги: ")
            lib.return_book(bid)

        elif choice == "7":
            uid = input("ID пользователя: ")
            lib.show_user_history(uid)

        elif choice == "8":
            Storage.save(lib)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(lib)
            print("👋 Выход")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()