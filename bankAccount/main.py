import json


class BankAccount:
    def __init__(self, balance=0, history=None):
        self.balance = balance
        self.history = history if history is not None else []

    def deposit(self, amount):
        if amount <= 0:
            print("Сумма должна быть больше 0")
            return

        self.balance += amount
        self.history.append(f"+{amount} (пополнение)")
        print("Успешно пополнено")

    def withdraw(self, amount):
        if amount <= 0:
            print("Сумма должна быть больше 0")
            return

        if amount > self.balance:
            print("Недостаточно средств")
            return

        self.balance -= amount
        self.history.append(f"-{amount} (снятие)")
        print("Успешно снято")

    def show_balance(self):
        print(f"\n💳 Баланс: {self.balance}")

    def show_history(self):
        print("\n📜 История операций:")
        if not self.history:
            print("Операций нет")
            return

        for op in self.history:
            print(op)

    def to_dict(self):
        return {
            "balance": self.balance,
            "history": self.history
        }

    @staticmethod
    def from_dict(data):
        return BankAccount(
            data.get("balance", 0),
            data.get("history", [])
        )

    def __str__(self):
        return f"Баланс: {self.balance}"


class BankStorage:
    FILE_NAME = "bank_account.json"

    @staticmethod
    def save(account):
        with open(BankStorage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(account.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load():
        try:
            with open(BankStorage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                return BankAccount.from_dict(data)
        except FileNotFoundError:
            return BankAccount()


def main():
    account = BankStorage.load()

    if account.history:
        print("Данные загружены")
    else:
        print("Создан новый счёт")

    while True:
        print("\n=== 💳 БАНКОВСКИЙ СЧЁТ ===")
        print("1. Пополнить")
        print("2. Снять")
        print("3. Баланс")
        print("4. История")
        print("5. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            try:
                amount = float(input("Сумма: "))
                account.deposit(amount)
            except ValueError:
                print("Ошибка: введите число")

        elif choice == "2":
            try:
                amount = float(input("Сумма: "))
                account.withdraw(amount)
            except ValueError:
                print("Ошибка: введите число")

        elif choice == "3":
            account.show_balance()

        elif choice == "4":
            account.show_history()

        elif choice == "5":
            BankStorage.save(account)
            print("💾 Сохранено")

        elif choice == "0":
            BankStorage.save(account)
            print("👋 Выход + сохранение")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()