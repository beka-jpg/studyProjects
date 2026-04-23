import json
from datetime import datetime


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name
        }

    @staticmethod
    def from_dict(data):
        return User(
            data["user_id"],
            data["name"]
        )

    def __str__(self):
        return f"{self.user_id} | {self.name}"


class Message:
    def __init__(self, sender_id, receiver_id, text, timestamp=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.text = text
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S") # yyyy-MM-dd HH:MM:SS

    def to_dict(self):
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "text": self.text,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Message(
            data["sender_id"],
            data["receiver_id"],
            data["text"],
            data.get("timestamp")
        )

    def __str__(self):
        return f"[{self.timestamp}] {self.sender_id} -> {self.receiver_id}: {self.text}"


class ChatSystem:
    def __init__(self):
        self.users = []
        self.messages = []

    def find_user(self, user_id):
        for u in self.users:
            if u.user_id == user_id:
                return u
        return None

    def add_user(self, user):
        if self.find_user(user.user_id):
            print("❌ Пользователь уже существует")
            return
        self.users.append(user)
        print("👤 Пользователь добавлен")

    def show_users(self):
        if not self.users:
            print("Нет пользователей")
            return
        for u in self.users:
            print(u)

    def send_message(self, sender_id, receiver_id, text):
        sender = self.find_user(sender_id)
        receiver = self.find_user(receiver_id)

        if not sender or not receiver:
            print("❌ Пользователь не найден")
            return

        msg = Message(sender_id, receiver_id, text)
        self.messages.append(msg)
        print("✉ Сообщение отправлено")

    def show_chat(self, user1, user2):
        print(f"\n💬 Чат {user1} <-> {user2}")

        found = False
        for m in self.messages:
            if (
                (m.sender_id == user1 and m.receiver_id == user2) or
                (m.sender_id == user2 and m.receiver_id == user1)
            ):
                print(m)
                found = True

        if not found:
            print("Нет сообщений")

    def to_dict(self):
        return {
            "users": [u.to_dict() for u in self.users],
            "messages": [m.to_dict() for m in self.messages]
        }

    def from_dict(self, data):
        self.users = [User.from_dict(u) for u in data.get("users", [])]
        self.messages = [Message.from_dict(m) for m in data.get("messages", [])]


class Storage:
    FILE_NAME = "chat.json"

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
            print("📂 Новый чат")


def main():
    system = ChatSystem()
    Storage.load(system)

    while True:
        print("\n=== 💬 ЧАТ ===")
        print("1. Добавить пользователя")
        print("2. Показать пользователей")
        print("3. Отправить сообщение")
        print("4. Показать чат")
        print("5. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            uid = input("ID: ")
            name = input("Имя: ")
            system.add_user(User(uid, name))

        elif choice == "2":
            system.show_users()

        elif choice == "3":
            system.send_message(
                input("От кого (ID): "),
                input("Кому (ID): "),
                input("Сообщение: ")
            )

        elif choice == "4":
            system.show_chat(
                input("ID пользователя 1: "),
                input("ID пользователя 2: ")
            )

        elif choice == "5":
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