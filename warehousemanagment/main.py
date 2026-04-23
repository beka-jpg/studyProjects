import json


class Product:
    def __init__(self, product_id, name, quantity=0):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity

    def add_stock(self, amount):
        if amount <= 0:
            print("❌ Количество должно быть больше 0")
            return False
        self.quantity += amount
        return True

    def remove_stock(self, amount):
        if amount <= 0:
            print("❌ Количество должно быть больше 0")
            return False
        if amount > self.quantity:
            print("❌ Недостаточно товара на складе")
            return False
        self.quantity -= amount
        return True

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "quantity": self.quantity
        }

    @staticmethod
    def from_dict(data):
        return Product(
            data["product_id"],
            data["name"],
            data.get("quantity", 0)
        )

    def __str__(self):
        return f"{self.product_id} | {self.name} | Остаток: {self.quantity}"


class Supply:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }

    @staticmethod
    def from_dict(data):
        return Supply(
            data["product_id"],
            data["quantity"]
        )


class Warehouse:
    def __init__(self):
        self.products = []
        self.supplies = []

    def find_product(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    def add_product(self, product):
        if self.find_product(product.product_id):
            print("❌ Товар уже существует")
            return
        self.products.append(product)
        print("📦 Товар добавлен")

    def show_products(self):
        if not self.products:
            print("Склад пуст")
            return
        for p in self.products:
            print(p)

    def supply_product(self, product_id, quantity):
        product = self.find_product(product_id)
        if not product:
            print("Товар не найден")
            return

        if product.add_stock(quantity):
            self.supplies.append(Supply(product_id, quantity))
            print("🚚 Поставка выполнена")

    def ship_product(self, product_id, quantity):
        product = self.find_product(product_id)
        if not product:
            print("❌ Товар не найден")
            return

        if product.remove_stock(quantity):
            print("📤 Товар отгружен")

    def show_supplies(self):
        if not self.supplies:
            print("Нет поставок")
            return

        print("\n📋 История поставок:")
        for s in self.supplies:
            print(f"{s.product_id} | +{s.quantity}")

    def to_dict(self):
        return {
            "products": [p.to_dict() for p in self.products],
            "supplies": [s.to_dict() for s in self.supplies]
        }

    def from_dict(self, data):
        self.products = [Product.from_dict(p) for p in data.get("products", [])]
        self.supplies = [Supply.from_dict(s) for s in data.get("supplies", [])]


class Storage:
    FILE_NAME = "warehouse.json"

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
            print("📂 Новый склад")


def main():
    warehouse = Warehouse()
    Storage.load(warehouse)

    while True:
        print("\n=== 📦 СКЛАД ===")
        print("1. Добавить товар")
        print("2. Показать товары")
        print("3. Поставка")
        print("4. Отгрузка")
        print("5. История поставок")
        print("6. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            pid = input("ID: ")
            name = input("Название: ")
            warehouse.add_product(Product(pid, name))

        elif choice == "2":
            warehouse.show_products()

        elif choice == "3":
            warehouse.supply_product(
                input("ID товара: "),
                int(input("Количество: "))
            )

        elif choice == "4":
            warehouse.ship_product(
                input("ID товара: "),
                int(input("Количество: "))
            )

        elif choice == "5":
            warehouse.show_supplies()

        elif choice == "6":
            Storage.save(warehouse)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(warehouse)
            print("👋 Выход")
            break

        else:
            print("❌ Неверный выбор")


if __name__ == "__main__":
    main()