import json


class Task:
    def __init__(self, title, priority="Средний"):
        self.title = title
        self.priority = priority
        self.done = False

    def mark_done(self):
        self.done = True

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "done": self.done
        }

    @staticmethod
    def from_dict(data):
        task = Task(data["title"], data.get("priority", "Средний"))
        task.done = data.get("done", False)
        return task

    def __str__(self):
        status = "Готово" if self.done else "Сделать"
        return f"{self.title} | {self.priority} | {status}"



class TaskManager:
    def __init__(self):
        self.tasks = []

    def find_task(self, title):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        return None


    def add_task(self, task):
        if self.find_task(task.title):
            print("Задача уже существует")
            return

        self.tasks.append(task)
        print("📝 Задача добавлена")


    def show_tasks(self):
        if not self.tasks:
            print("Список пуст")
            return

        for i, t in enumerate(self.sorted_tasks(), 1):
            print(f"{i}. {t}")

    def sorted_tasks(self):
        priority_order = {"Высокий": 0, "Средний": 1, "Низкий": 2}

        return sorted(
            self.tasks,
            key=lambda x: priority_order.get(x.priority, 1)
        )


    def mark_done(self, title):
        task = self.find_task(title)
        if not task:
            print("Задача не найдена")
            return

        task.mark_done()
        print("Отмечено выполненной")

    def change_priority(self, title, priority):
        task = self.find_task(title)
        if not task:
            print(" Задача не найдена")
            return

        task.priority = priority
        print("🔄 Приоритет обновлён")


    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            print(f"🗑 Удалено: {removed.title}")
        else:
            print(" Ошибка индекса")


    def to_dict(self):
        return [t.to_dict() for t in self.tasks]

    def from_dict(self, data):
        self.tasks = [Task.from_dict(t) for t in data]



class Storage:
    FILE_NAME = "tasks.json"

    @staticmethod
    def save(manager):
        with open(Storage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(manager.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(manager):
        try:
            with open(Storage.FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                manager.from_dict(data)
        except FileNotFoundError:
            print("📂 Новый список задач")


def main():
    manager = TaskManager()
    Storage.load(manager)

    while True:
        print("\n=== Список задач ===")
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Выполнить задачу")
        print("4. Изменить приоритет")
        print("5. Удалить задачу")

        print("\n7. Сохранить")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            title = input("Название: ")
            priority = input("Приоритет (Высокий/Средний/Низкий): ").upper()

            if priority not in ["Высокий", "Средний", "Низкий"]:
                priority = "Средний"

            manager.add_task(Task(title, priority))

        elif choice == "2":
            manager.show_tasks()

        elif choice == "3":
            manager.mark_done(input("Название задачи: "))

        elif choice == "4":
            title = input("Название: ")
            priority = input("Новый приоритет: ").upper()

            if priority not in ["Высокий", "Средний", "Низкий"]:
                print("Неверный приоритет")
            else:
                manager.change_priority(title, priority)

        elif choice == "5":
            manager.show_tasks()
            try:
                index = int(input("Номер: ")) - 1
                manager.delete_task(index)
            except ValueError:
                print("Ошибка ввода")

        elif choice == "7":
            Storage.save(manager)
            print("💾 Сохранено")

        elif choice == "0":
            Storage.save(manager)
            print("👋 Выход")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()