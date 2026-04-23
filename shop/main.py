import json


class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def add_stock(self, amount):
        if amount <= 0:
            print("Количество должно быть > 0")
            return

        self.quantity += amount
        print(f"Добавлено. Теперь: {self.quantity}")

    def buy(self, amount):
        if amount <= 0:
            print("Неверное количество")
            return False

        if amount > self.quantity:
            print("Недостаточно товара")
            return False

        self.quantity -= amount
        total = self.price * amount
        print(f"Куплено на сумму: {total}")
        return True

    def change_price(self, new_price):
        if new_price <= 0:
            print("Цена должна быть > 0")
            return

        self.price = new_price
        print(f"Новая цена: {self.price}")

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    @staticmethod
    def from_dict(data):
        return Product(
            data["product_id"],
            data["name"],
            data["price"],
            data["quantity"]
        )

    def __str__(self):
        return f"{self.product_id} | {self.name} | {self.price} | Остаток: {self.quantity}"


class Store:
    def __init__(self):
        self.products = []


    def find_by_id(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    def find_by_name(self, name):
        for p in self.products:
            if p.name.lower() == name.lower():
                return p
        return None


    def add_product(self, product):
        if self.find_by_id(product.product_id):
            print("ID уже существует")
            return

        if self.find_by_name(product.name):
            print("Такой товар уже существует")
            return

        self.products.append(product)
        print("Товар добавлен")

    def show_products(self):
        if not self.products:
            print("Магазин пуст")
            return

        for i, p in enumerate(self.products, 1):
            print(f"{i}. {p}")


    def update_product(self, product_id):
        product = self.find_by_id(product_id)
        if not product:
            print("❌ Товар не найден")
            return

        print("1. Изменить цену")
        print("2. Пополнить склад")

        choice = input("Выбор: ")

        if choice == "1":
            try:
                price = float(input("Новая цена: "))
                product.change_price(price)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "2":
            try:
                amount = int(input("Количество: "))
                product.add_stock(amount)
            except ValueError:
                print("Ошибка ввода")


    def delete_product(self, index):
        if 0 <= index < len(self.products):
            removed = self.products.pop(index)
            print(f"🗑 Удалён: {removed.name}")
        else:
            print("❌ Ошибка индекса")


    def buy_product(self, product_id, amount):
        product = self.find_by_id(product_id)
        if not product:
            print("❌ Товар не найден")
            return

        product.buy(amount)


    def search(self, keyword):
        results = [
            p for p in self.products
            if keyword.lower() in p.name.lower()
        ]

        if not results:
            print("Ничего не найдено")
            return

        for p in results:
            print(p)


    def to_dict(self):
        return [p.to_dict() for p in self.products]

    def from_dict(self, data):
        self.products = [Product.from_dict(p) for p in data]


class Storage:
    FILE_NAME = "store.json"

    @staticmethod
    def save(store):
        with open(Storage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(store.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(store):
        try:
            with open(Storage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                store.from_dict(data)
        except FileNotFoundError:
            print("📂 Новый магазин")



def main():
    store = Store()
    Storage.load(store)

    while True:
        print("\n=== 🛒 МАГАЗИН ===")
        print("1. Добавить товар")
        print("2. Показать товары")
        print("3. Купить товар")
        print("4. Изменить товар")
        print("5. Удалить товар")
        print("6. Поиск")

        print("\n7. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            product_id = input("ID: ")
            name = input("Название: ")

            try:
                price = float(input("Цена: "))
                quantity = int(input("Количество: "))
            except ValueError:
                print("Ошибка ввода")
                continue

            store.add_product(Product(product_id, name, price, quantity))

        elif choice == "2":
            store.show_products()

        elif choice == "3":
            product_id = input("ID товара: ")
            try:
                amount = int(input("Количество: "))
                store.buy_product(product_id, amount)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "4":
            product_id = input("ID товара: ")
            store.update_product(product_id)

        elif choice == "5":
            store.show_products()
            try:
                index = int(input("Номер: ")) - 1
                store.delete_product(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "6":
            keyword = input("Поиск: ")
            store.search(keyword)

        elif choice == "7":
            Storage.save(store)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(store)
            print("👋 Выход + сохранение")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()