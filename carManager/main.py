import json


class Car:
    def __init__(self, brand, speed=0):
        self.brand = brand
        self.speed = speed
        self.is_moving = False

    def start(self):
        if self.is_moving:
            print("🚗 Машина уже движется")
            return

        self.is_moving = True
        print(f"🚗 {self.brand} начала движение")

    def stop(self):
        if not self.is_moving:
            print("🛑 Машина уже стоит")
            return

        self.is_moving = False
        self.speed = 0
        print(f"🛑 {self.brand} остановилась")

    def accelerate(self, value):
        if not self.is_moving:
            print("Сначала нужно начать движение")
            return

        if value <= 0:
            print("Скорость должна быть > 0")
            return

        self.speed += value
        print(f"⚡ {self.brand} ускорилась до {self.speed} км/ч")

    def to_dict(self):
        return {
            "brand": self.brand,
            "speed": self.speed,
            "is_moving": self.is_moving
        }

    @staticmethod
    def from_dict(data):
        car = Car(data["brand"], data.get("speed", 0))
        car.is_moving = data.get("is_moving", False)
        return car

    def __str__(self):
        status = "едет" if self.is_moving else "стоит"
        return f"{self.brand} | {self.speed} км/ч | {status}"


class Garage:
    def __init__(self):
        self.cars = []


    def find_car(self, brand):
        for c in self.cars:
            if c.brand.lower() == brand.lower():
                return c
        return None

    def add_car(self, car):
        if self.find_car(car.brand):
            print("Такая машина уже существует")
            return

        self.cars.append(car)
        print("🚗 Машина добавлена")


    def show_cars(self):
        if not self.cars:
            print("Гараж пуст")
            return

        for i, c in enumerate(self.cars, 1):
            print(f"{i}. {c}")

    def delete_car(self, index):
        if 0 <= index < len(self.cars):
            removed = self.cars.pop(index)
            print(f"🗑 Удалена: {removed.brand}")
        else:
            print("❌ Ошибка индекса")


    def start_car(self, brand):
        car = self.find_car(brand)
        if not car:
            print("Машина не найдена")
            return

        car.start()

    def stop_car(self, brand):
        car = self.find_car(brand)
        if not car:
            print("Машина не найдена")
            return

        car.stop()

    def accelerate_car(self, brand, value):
        car = self.find_car(brand)
        if not car:
            print("Машина не найдена")
            return

        car.accelerate(value)

    def to_dict(self):
        return [c.to_dict() for c in self.cars]

    def from_dict(self, data):
        self.cars = [Car.from_dict(c) for c in data]


class Storage:
    FILE_NAME = "garage.json"

    @staticmethod
    def save(garage):
        with open(Storage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(garage.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(garage):
        try:
            with open(Storage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                garage.from_dict(data)
        except FileNotFoundError:
            print("📂 Новый гараж создан")


def main():
    garage = Garage()
    Storage.load(garage)

    while True:
        print("\n===ГАРАЖ ===")
        print("1. Добавить машину")
        print("2. Показать машины")
        print("3. Удалить машину")

        print("\n--- Движение ---")
        print("4. Завести машину")
        print("5. Остановить машину")
        print("6. Ускорить машину")

        print("\n7. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            brand = input("Марка: ")
            garage.add_car(Car(brand))

        elif choice == "2":
            garage.show_cars()

        elif choice == "3":
            garage.show_cars()
            try:
                index = int(input("Номер: ")) - 1
                garage.delete_car(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "4":
            brand = input("Марка: ")
            garage.start_car(brand)

        elif choice == "5":
            brand = input("Марка: ")
            garage.stop_car(brand)

        elif choice == "6":
            brand = input("Марка: ")
            try:
                speed = int(input("Скорость: "))
                garage.accelerate_car(brand, speed)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "7":
            Storage.save(garage)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(garage)
            print("👋 Выход + сохранение")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()