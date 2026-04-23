import json



class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def reduce_stock(self, qty):
        if qty > self.stock:
            return False
        self.stock -= qty
        return True

    def increase_stock(self, qty):
        self.stock += qty

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

    @staticmethod
    def from_dict(data):
        return Product(
            data["product_id"],
            data["name"],
            data["price"],
            data.get("stock", 0)
        )

    def __str__(self):
        return f"{self.product_id} | {self.name} | {self.price} | stock: {self.stock}"


class CartItem:
    def __init__(self, product, qty):
        self.product = product
        self.qty = qty

    def total(self):
        return self.product.price * self.qty

    def __str__(self):
        return f"{self.product.name} x{self.qty} = {self.total()}"


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product, qty):
        if qty <= 0:
            print("Неверное количество")
            return

        # если уже есть товар — увеличиваем
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.qty += qty
                return

        self.items.append(CartItem(product, qty))

    def remove(self, product_id):
        self.items = [
            item for item in self.items
            if item.product.product_id != product_id
        ]

    def clear(self):
        self.items = []

    def total(self):
        return sum(i.total() for i in self.items)

    def show(self):
        if not self.items:
            print("Корзина пуста")
            return

        for i in self.items:
            print(i)

        print(f"\nИТОГО: {self.total()}")



class Store:
    def __init__(self):
        self.products = []
        self.cart = Cart()
        self.orders = []


    def find_product(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None


    def add_product(self, product):
        if self.find_product(product.product_id):
            print(" Такой товар уже есть")
            return

        self.products.append(product)
        print("📦 Товар добавлен")

    def show_products(self):
        if not self.products:
            print("Каталог пуст")
            return

        for p in self.products:
            print(p)


    def add_to_cart(self, product_id, qty):
        product = self.find_product(product_id)

        if not product:
            print("Товар не найден")
            return

        if qty > product.stock:
            print(" Недостаточно товара")
            return

        self.cart.add(product, qty)
        print("🛒 Добавлено в корзину")

    def show_cart(self):
        self.cart.show()


    def checkout(self):
        if not self.cart.items:
            print("Корзина пуста")
            return

        # проверка и списание
        for item in self.cart.items:
            if item.qty > item.product.stock:
                print(f"❌ Недостаточно: {item.product.name}")
                return

        for item in self.cart.items:
            item.product.reduce_stock(item.qty)

        order = {
            "items": [
                {
                    "product": item.product.name,
                    "qty": item.qty,
                    "total": item.total()
                }
                for item in self.cart.items
            ],
            "total": self.cart.total()
        }

        self.orders.append(order)
        self.cart.clear()

        print("Заказ оформлен")

    def show_orders(self):
        if not self.orders:
            print("Нет заказов")
            return

        for i, o in enumerate(self.orders, 1):
            print(f"\nЗаказ {i}")
            for item in o["items"]:
                print(f"  {item['product']} x{item['qty']} = {item['total']}")
            print(f"ИТОГО: {o['total']}")


    def to_dict(self):
        return {
            "products": [p.to_dict() for p in self.products],
            "orders": self.orders
        }

    def from_dict(self, data):
        self.products = [Product.from_dict(p) for p in data.get("products", [])]
        self.orders = data.get("orders", [])


class Storage:
    FILE_NAME = "shop.json"

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
        print("\n=== 🛍 ИНТЕРНЕТ-МАГАЗИН ===")
        print("1. Добавить товар")
        print("2. Показать каталог")
        print("3. Добавить в корзину")
        print("4. Показать корзину")
        print("5. Оформить заказ")
        print("6. Показать заказы")

        print("\n7. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            pid = input("ID: ")
            name = input("Название: ")
            price = float(input("Цена: "))
            stock = int(input("Количество: "))
            store.add_product(Product(pid, name, price, stock))

        elif choice == "2":
            store.show_products()

        elif choice == "3":
            pid = input("ID товара: ")
            qty = int(input("Количество: "))
            store.add_to_cart(pid, qty)

        elif choice == "4":
            store.show_cart()

        elif choice == "5":
            store.checkout()

        elif choice == "6":
            store.show_orders()

        elif choice == "7":
            Storage.save(store)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(store)
            print("👋 Выход")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()