import json



class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def reduce_stock(self, amount):
        if amount > self.quantity:
            return False
        self.quantity -= amount
        return True

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
            data.get("quantity", 0)
        )

    def __str__(self):
        return f"{self.product_id} | {self.name} | {self.price} | Остаток: {self.quantity}"



class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name
        }

    @staticmethod
    def from_dict(data):
        return Customer(data["customer_id"], data["name"])

    def __str__(self):
        return f"{self.customer_id} | {self.name}"


class OrderItem:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total(self):
        return self.price * self.quantity

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    @staticmethod
    def from_dict(data):
        return OrderItem(
            data["product_id"],
            data["name"],
            data["price"],
            data["quantity"]
        )

    def __str__(self):
        return f"{self.name} x{self.quantity} = {self.get_total()}"



class Order:
    def __init__(self, order_id, customer_id):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_total(self):
        return sum(i.get_total() for i in self.items)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": [i.to_dict() for i in self.items]
        }

    @staticmethod
    def from_dict(data):
        order = Order(data["order_id"], data["customer_id"])
        order.items = [OrderItem.from_dict(i) for i in data.get("items", [])]
        return order

    def __str__(self):
        result = f"\nЗаказ {self.order_id} (клиент {self.customer_id})\n"
        for item in self.items:
            result += f"  {item}\n"
        result += f"Итого: {self.get_total()}"
        return result


class OrderSystem:
    def __init__(self):
        self.products = []
        self.customers = []
        self.orders = []


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
            print("Нет товаров")
            return

        for p in self.products:
            print(p)


    def find_customer(self, customer_id):
        for c in self.customers:
            if c.customer_id == customer_id:
                return c
        return None

    def add_customer(self, customer):
        if self.find_customer(customer.customer_id):
            print("Клиент уже существует")
            return

        self.customers.append(customer)
        print("Клиент добавлен")

    def show_customers(self):
        if not self.customers:
            print("Нет клиентов")
            return

        for c in self.customers:
            print(c)


    def create_order(self, order_id, customer_id):
        if self.find_customer(customer_id) is None:
            print("Клиент не найден")
            return

        order = Order(order_id, customer_id)

        while True:
            self.show_products()
            product_id = input("ID товара (или 0 для выхода): ")

            if product_id == "0":
                break

            product = self.find_product(product_id)
            if not product:
                print("Товар не найден")
                continue

            try:
                qty = int(input("Количество: "))
            except ValueError:
                print("Ошибка")
                continue

            if qty <= 0:
                print("Количество должно быть > 0")
                continue

            if not product.reduce_stock(qty):
                print("Недостаточно товара на складе")
                continue

            order.add_item(
                OrderItem(product.product_id, product.name, product.price, qty)
            )

        if order.items:
            self.orders.append(order)
            print("Заказ создан")
        else:
            print("Пустой заказ не сохранён")

    def show_orders(self):
        if not self.orders:
            print("Нет заказов")
            return

        for o in self.orders:
            print(o)


    def to_dict(self):
        return {
            "products": [p.to_dict() for p in self.products],
            "customers": [c.to_dict() for c in self.customers],
            "orders": [o.to_dict() for o in self.orders]
        }

    def from_dict(self, data):
        self.products = [Product.from_dict(p) for p in data.get("products", [])]
        self.customers = [Customer.from_dict(c) for c in data.get("customers", [])]
        self.orders = [Order.from_dict(o) for o in data.get("orders", [])]


class Storage:
    FILE_NAME = "orders.json"

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
            print("📂 Новая система заказов")



def main():
    system = OrderSystem()
    Storage.load(system)

    while True:
        print("\n=== 🧾 СИСТЕМА ЗАКАЗОВ ===")
        print("1. Добавить товар")
        print("2. Добавить клиента")
        print("3. Показать товары")
        print("4. Показать клиентов")
        print("5. Создать заказ")
        print("6. Показать заказы")

        print("\n7. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            pid = input("ID: ")
            name = input("Название: ")
            try:
                price = float(input("Цена: "))
                qty = int(input("Количество: "))
            except ValueError:
                print("Ошибка ввода")
                continue

            system.add_product(Product(pid, name, price, qty))

        elif choice == "2":
            cid = input("ID клиента: ")
            name = input("Имя: ")
            system.add_customer(Customer(cid, name))

        elif choice == "3":
            system.show_products()

        elif choice == "4":
            system.show_customers()

        elif choice == "5":
            oid = input("ID заказа: ")
            cid = input("ID клиента: ")
            system.create_order(oid, cid)

        elif choice == "6":
            system.show_orders()

        elif choice == "7":
            Storage.save(system)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(system)
            print("👋 Выход + сохранение")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()