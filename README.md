Дана бібліотека генерує конфігураційний файл для його використанні у https://github.com/uwine4850/yefgo.

Більш детальний приклад використання - https://github.com/uwine4850/yefexample.

## Приклад використання

Для того, щоб згенерувати конфігураційний файл потрібно зробити три речі:
- Ініціалізувати скрипт, який робить базове налаштування перед кожним запуском.
- Ініціалізувати модулі, які можна використовувати.
- Позначити класи та функції, які можуть бути використані.

Після даних маніпуляцій можна переходити, до використання даного проекту у [yefgo](https://github.com/uwine4850/yefgo).

### Створення скрипта
```
generate_start_sh("/home/fhx/GolandProjects/yefgotest/pyproj/.venv", ["/home/fhx/GolandProjects/yefgotest/pyproj"],
        "/home/fhx/GolandProjects/yefgotest/pygen")
```
Тут все дуже просто - потрібно передати шлях до ``venv``, шлях до кореня проекту та шлях до директорії, яка буде зберігати скрипт.

Далі скрипт потрібно запускати у кожній новій сесії використання [yefgo](https://github.com/uwine4850/yefgo).

### Ініціалізація модулів

```
shop = Module("proj.shop", "shop", "shop.go", [])
customer = Module("proj.customer", "customer", "customer.go", [])
```
Для початку потрібно створити екземпляр классу ``Module`` для модулів Python.

- Перший аргумент - це шлях імпорту модуля в Python.
- Другий аргумент - назва нового пакета у golang.
- Третій аргумент - назва файлу golang.
- Четвертий аргумент - список пакетів які потрібно імпортувати. Наприклад, якщо потрібно у пакет `customer` імпотрувати 
пакет `shop` - код буде виглядати так `Module("proj.customer", "customer", "customer.go", ["shop"])`. Важливо зазначити, 
що тут порібно вписувати саме назву пакету golang, тобто, те що у другому аргументі.

Далі потрібно згенерувати конфігураційний файл.
```
modules_info = get_modules_info([shop, customer])
yaml_modules_data = get_yaml_modules_data(modules_info)
generate_yaml(yaml_modules_data, "pygen.yaml", "/home/fhx/GolandProjects/yefgotest/pygen")
```
Тут все дуже просто, потрібно передати список модулів, перетворити дані про них в дані у форматі yaml, та згенеровати 
файл .yaml у вибраній директорії.

### Позначення класів та функцій

```
from proj.shop import Product, Shop
from yefpy import gotypes, yef


class Customer(yef.YefClass):
    @gotypes.gotype({"shop": "*goclass.Class"}, "")
    def __init__(self, shop: Shop):
        self.shop = shop

    @gotypes.gotype({"product": "*goclass.Class"}, "")
    def by_product(self, product: Product):
        self.shop.delete_products(product)
```
Для того, що зрибити кофігурацію для класу, потрібно успадкувати його від класу `yef.YefClass`. Тепер цей клас, та його 
методи будуть додані до файлу конфігурації.

Для того, щоб передати будь-який тип даних потрібно використовувати декоратор `@gotypes.gotype`. Даний декоратир 
призначений для того, щоб явно прописати у конфігураційному файлі тип даних golang. Тобто, для правильної роботи потрібно 
в ручну перевести тип даних Python у тип даних golang. Для передачі будь-якого класу(struct у golang) потрібно 
використовувати `*goclass.Class`.

Якщо метод повертає який тип даних, його потрібно записати у 
відповідному аргументі, наприклад, `@gotypes.gotype({"product": "*goclass.Class"}, "string")`. Важливо зазначити, що коли 
повертається тип даних класу(структури) потрібно вказати назву структури, а не `*goclass.Class`, наприклад, 
`@gotypes.gotype({"product": "*goclass.Class"}, "User")`.