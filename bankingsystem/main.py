import json


class BankAccount:
    def __init__(self, account_id, owner, balance=0):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            print("Сумма должна быть больше 0")
            return
        self.balance += amount
        self.history.append(f"+{amount} пополнение")
        print("Пополнение успешно")

    def withdraw(self, amount):
        if amount <= 0:
            print("Сумма должна быть больше 0")
            return
        if amount > self.balance:
            print("Недостаточно средств")
            return
        self.balance -= amount
        self.history.append(f"-{amount} снятие")
        print("Снятие успешно")

    def info(self):
        return f"{self.account_id} | {self.owner} | баланс: {self.balance}"

    def to_dict(self):
        return {
            "type": "BankAccount",
            "account_id": self.account_id,
            "owner": self.owner,
            "balance": self.balance,
            "history": self.history
        }

    @staticmethod
    def from_dict(data):
        acc = BankAccount(
            data["account_id"],
            data["owner"],
            data.get("balance", 0)
        )
        acc.history = data.get("history", [])
        return acc


class SavingsAccount(BankAccount):
    def __init__(self, account_id, owner, balance=0, interest=5):
        super().__init__(account_id, owner, balance)
        self.interest = interest

    def add_interest(self):
        profit = self.balance * self.interest / 100
        self.balance += profit
        self.history.append(f"проценты +{profit}")
        print(f"📈 Начислены проценты: {profit}")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "SavingsAccount"
        data["interest"] = self.interest
        return data

    @staticmethod
    def from_dict(data):
        acc = SavingsAccount(
            data["account_id"],
            data["owner"],
            data.get("balance", 0),
            data.get("interest", 5)
        )
        acc.history = data.get("history", [])
        return acc


class BankSystem:
    def __init__(self):
        self.accounts = []

    def find_account(self, account_id):
        for a in self.accounts:
            if a.account_id == account_id:
                return a
        return None

    def add_account(self, account):
        if self.find_account(account.account_id):
            print("❌ Счёт уже существует")
            return
        self.accounts.append(account)
        print("🏦 Счёт добавлен")

    def show_accounts(self):
        if not self.accounts:
            print("Нет счетов")
            return
        for a in self.accounts:
            print(a.info())

    def deposit(self, account_id, amount):
        acc = self.find_account(account_id)
        if not acc:
            print("❌ Счёт не найден")
            return
        acc.deposit(amount)

    def withdraw(self, account_id, amount):
        acc = self.find_account(account_id)
        if not acc:
            print("❌ Счёт не найден")
            return
        acc.withdraw(amount)

    def transfer(self, from_id, to_id, amount):
        sender = self.find_account(from_id)
        receiver = self.find_account(to_id)

        if not sender or not receiver:
            print("❌ Один из счетов не найден")
            return

        if amount <= 0:
            print("❌ Сумма должна быть больше 0")
            return

        if sender.balance < amount:
            print("❌ Недостаточно средств")
            return

        sender.balance -= amount
        receiver.balance += amount

        sender.history.append(f"перевод -{amount} -> {to_id}")
        receiver.history.append(f"перевод +{amount} <- {from_id}")

        print("🔁 Перевод выполнен успешно")

    def add_interest(self, account_id):
        acc = self.find_account(account_id)
        if not acc:
            print("❌ Счёт не найден")
            return
        if isinstance(acc, SavingsAccount):
            acc.add_interest()
        else:
            print("❌ Проценты доступны только для сберегательного счёта")

    def show_history(self, account_id):
        acc = self.find_account(account_id)
        if not acc:
            print("❌ Счёт не найден")
            return

        print(f"\n📜 История операций ({acc.owner}):")
        if not acc.history:
            print("Пусто")
            return

        for h in acc.history:
            print(" -", h)

    def to_dict(self):
        return [a.to_dict() for a in self.accounts]

    def from_dict(self, data):
        self.accounts = []
        for a in data:
            if a["type"] == "SavingsAccount":
                self.accounts.append(SavingsAccount.from_dict(a))
            else:
                self.accounts.append(BankAccount.from_dict(a))


class Storage:
    FILE_NAME = "bank.json"

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
            print("📂 Создана новая банковская система")


def main():
    bank = BankSystem()
    Storage.load(bank)

    while True:
        print("\n=== 🏦 БАНКОВСКАЯ СИСТЕМА ===")
        print("1. Создать обычный счёт")
        print("2. Создать сберегательный счёт")
        print("3. Показать счета")
        print("4. Пополнить счёт")
        print("5. Снять деньги")
        print("6. Перевод между счетами")
        print("7. Начислить проценты")
        print("8. История операций")
        print("9. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            acc_id = input("ID счёта: ")
            owner = input("Владелец: ")
            bank.add_account(BankAccount(acc_id, owner))

        elif choice == "2":
            acc_id = input("ID счёта: ")
            owner = input("Владелец: ")
            interest = float(input("Процент (%): "))
            bank.add_account(SavingsAccount(acc_id, owner, 0, interest))

        elif choice == "3":
            bank.show_accounts()

        elif choice == "4":
            bank.deposit(input("ID счёта: "), float(input("Сумма: ")))

        elif choice == "5":
            bank.withdraw(input("ID счёта: "), float(input("Сумма: ")))

        elif choice == "6":
            bank.transfer(
                input("С какого счёта (ID): "),
                input("На какой счёт (ID): "),
                float(input("Сумма: "))
            )

        elif choice == "7":
            bank.add_interest(input("ID счёта: "))

        elif choice == "8":
            bank.show_history(input("ID счёта: "))

        elif choice == "9":
            Storage.save(bank)
            print("💾 Данные сохранены")

        elif choice == "0":
            Storage.save(bank)
            print("👋 Выход из системы")
            break

        else:
            print("❌ Неверный выбор")


if __name__ == "__main__":
    main()