import json



class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.hunger = 0  # 0 = сытый, 100 = очень голодный

    def eat(self):
        self.hunger = max(0, self.hunger - 20)
        print(f"{self.name} поел. Сытость: {100 - self.hunger}")

    def make_sound(self):
        print("Животное издаёт звук")

    def info(self):
        return f"{self.name} | возраст: {self.age}"

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "age": self.age,
            "hunger": self.hunger
        }

    @staticmethod
    def from_dict(data):
        if data["type"] == "Cat":
            animal = Cat(data["name"], data["age"])
        elif data["type"] == "Dog":
            animal = Dog(data["name"], data["age"])
        else:
            return None

        animal.hunger = data.get("hunger", 0)
        return animal


class Cat(Animal):
    def make_sound(self):
        print(f"{self.name}: Мяу ...")

    def play(self):
        self.hunger += 10
        print(f"{self.name} играет (голод увеличился)")



class Dog(Animal):
    def make_sound(self):
        print(f"{self.name}: Гав ...")

    def play(self):
        self.hunger += 15
        print(f"{self.name} бегает (голод увеличился)")



class Zoo:
    def __init__(self):
        self.animals = []


    def find_animal(self, name):
        for a in self.animals:
            if a.name.lower() == name.lower():
                return a
        return None


    def add_animal(self, animal):
        if self.find_animal(animal.name):
            print("Животное с таким именем уже есть")
            return

        self.animals.append(animal)
        print("Добавлено")


    def show_animals(self):
        if not self.animals:
            print("Нет животных")
            return

        for i, a in enumerate(self.animals, 1):
            print(f"{i}. {a.info()} ({a.__class__.__name__})")


    def delete_animal(self, index):
        if 0 <= index < len(self.animals):
            removed = self.animals.pop(index)
            print(f"🗑 Удалено: {removed.name}")
        else:
            print("Ошибка индекса")


    def feed(self, name):
        animal = self.find_animal(name)
        if not animal:
            print("Не найдено")
            return

        animal.eat()

    def play(self, name):
        animal = self.find_animal(name)
        if not animal:
            print("Не найдено")
            return

        if hasattr(animal, "play"):
            animal.play()

    def sound(self, name):
        animal = self.find_animal(name)
        if not animal:
            print("Не найдено")
            return

        animal.make_sound()


    def to_dict(self):
        return [a.to_dict() for a in self.animals]

    def from_dict(self, data):
        self.animals = []
        for a in data:
            animal = Animal.from_dict(a)
            if animal:
                self.animals.append(animal)


class Storage:
    FILE_NAME = "animals.json"

    @staticmethod
    def save(zoo):
        with open(Storage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(zoo.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(zoo):
        try:
            with open(Storage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                zoo.from_dict(data)
        except FileNotFoundError:
            print("📂 Новый список животных")



def main():
    zoo = Zoo()
    Storage.load(zoo)

    while True:
        print("\n=== 🐾 ЖИВОТНЫЕ ===")
        print("1. Добавить кота")
        print("2. Добавить собаку")
        print("3. Показать всех")
        print("4. Покормить")
        print("5. Играть")
        print("6. Звук")
        print("7. Удалить")

        print("\n8. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            name = input("Имя: ")
            age = int(input("Возраст: "))
            zoo.add_animal(Cat(name, age))

        elif choice == "2":
            name = input("Имя: ")
            age = int(input("Возраст: "))
            zoo.add_animal(Dog(name, age))

        elif choice == "3":
            zoo.show_animals()

        elif choice == "4":
            zoo.feed(input("Имя: "))

        elif choice == "5":
            zoo.play(input("Имя: "))

        elif choice == "6":
            zoo.sound(input("Имя: "))

        elif choice == "7":
            zoo.show_animals()
            try:
                index = int(input("Номер: ")) - 1
                zoo.delete_animal(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "8":
            Storage.save(zoo)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(zoo)
            print("Выход + сохранение")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()