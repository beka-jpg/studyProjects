### Класс `Employee`
Описывает сотрудника:

- `emp_id` — уникальный ID  
- `name` — имя  
- `position` — должность  
- `salary` — зарплата  
- `email` — email  


Методы:
- `raise_salary(amount)` — увеличение зарплаты  
- `change_position(new_position)` — смена должности  
- `to_dict()` / `from_dict()` — сериализация из/с json

### Класс `Company`
Управляет списком сотрудников:

Методы:
- `add_employee()` — добавить сотрудника  
- `show_employees()` — показать всех  
- `find_by_id()` — поиск по ID  
- `find_by_email()` — поиск по email  
- `update_employee()` — редактирование  
- `delete_employee()` — удаление  
- `search()` — поиск по ключевому слову



Пример хранение данных в json

Формат:
```json
[
    {
        "emp_id": "1",
        "name": "Alex",
        "position": "Developer",
        "salary": 1200,
        "email": "alex@mail.com"
    }
]
