import json


class Ticket:
    def __init__(self, ticket_id, event_name, seat):
        self.ticket_id = ticket_id
        self.event_name = event_name
        self.seat = seat
        self.is_booked = False
        self.booked_by = None

    def book(self, user_name):
        if self.is_booked:
            return False

        self.is_booked = True
        self.booked_by = user_name
        return True

    def cancel(self):
        if not self.is_booked:
            return False

        self.is_booked = False
        self.booked_by = None
        return True

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "event_name": self.event_name,
            "seat": self.seat,
            "is_booked": self.is_booked,
            "booked_by": self.booked_by
        }

    @staticmethod
    def from_dict(data):
        t = Ticket(
            data["ticket_id"],
            data["event_name"],
            data["seat"]
        )
        t.is_booked = data.get("is_booked", False)
        t.booked_by = data.get("booked_by")
        return t

    def __str__(self):
        status = "ЗАНЯТ" if self.is_booked else "СВОБОДЕН"
        user = f" | {self.booked_by}" if self.booked_by else ""
        return f"{self.ticket_id} | {self.event_name} | место {self.seat} | {status}{user}"


class BookingSystem:
    def __init__(self):
        self.tickets = []
        self.users = []

    def find_ticket(self, ticket_id):
        for t in self.tickets:
            if t.ticket_id == ticket_id:
                return t
        return None

    def add_ticket(self, ticket):
        if self.find_ticket(ticket.ticket_id):
            print(" Билет уже существует")
            return
        self.tickets.append(ticket)
        print("🎫 Билет добавлен")

    def show_tickets(self):
        if not self.tickets:
            print("Нет билетов")
            return

        for t in self.tickets:
            print(t)

    def book_ticket(self, ticket_id, user_name):
        ticket = self.find_ticket(ticket_id)

        if not ticket:
            print("Билет не найден")
            return

        if ticket.book(user_name):
            print("Билет забронирован")
        else:
            print("❌ Уже забронирован")

    def cancel_booking(self, ticket_id):
        ticket = self.find_ticket(ticket_id)

        if not ticket:
            print("❌ Билет не найден")
            return

        if ticket.cancel():
            print("🔄 Бронь отменена")
        else:
            print(" Билет не был забронирован")

    def show_user_tickets(self, user_name):
        found = False
        print(f"\n🎟 Билеты пользователя {user_name}:")
        for t in self.tickets:
            if t.booked_by == user_name:
                print(t)
                found = True

        if not found:
            print("Пусто")

    def to_dict(self):
        return [t.to_dict() for t in self.tickets]

    def from_dict(self, data):
        self.tickets = [Ticket.from_dict(t) for t in data]


class Storage:
    FILE_NAME = "tickets.json"

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
            print("📂 Новая система бронирования")


def main():
    system = BookingSystem()
    Storage.load(system)

    while True:
        print("\n=== 🎫 БРОНИРОВАНИЕ БИЛЕТОВ ===")
        print("1. Добавить билет")
        print("2. Показать билеты")
        print("3. Забронировать билет")
        print("4. Отменить бронь")
        print("5. Билеты пользователя")
        print("6. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            tid = input("ID билета: ")
            event = input("Событие: ")
            seat = input("Место: ")
            system.add_ticket(Ticket(tid, event, seat))

        elif choice == "2":
            system.show_tickets()

        elif choice == "3":
            system.book_ticket(
                input("ID билета: "),
                input("Имя пользователя: ")
            )

        elif choice == "4":
            system.cancel_booking(input("ID билета: "))

        elif choice == "5":
            system.show_user_tickets(input("Имя пользователя: "))

        elif choice == "6":
            Storage.save(system)
            print("Сохранено")

        elif choice == "0":
            Storage.save(system)
            print("👋 Выход")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()