class RoomObject:
    """Базовий клас для будь-якого предмета в кімнаті."""

    def __init__(self, name="Предмет", coordinates=None):
        self._name = name
        # масив координат: список кортежів (x, y) — кути/опорні точки предмета
        self._coordinates = list(coordinates) if coordinates else []
        print(f"[+] Створено: {self._name}")

    def __del__(self):
        print(f"[-] Знищено: {self._name}")

    # ---- функції доступу ----
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_coordinates(self):
        return list(self._coordinates)

    def set_coordinates(self, coordinates):
        self._coordinates = list(coordinates)

    # ---- додаткова поведінка ----
    def move(self, dx, dy):
        """Зсунути всі точки предмета на (dx, dy)."""
        self._coordinates = [(x + dx, y + dy) for (x, y) in self._coordinates]

    def show(self):
        print(f"{self._name}: координати = {self._coordinates}")


class Bed(RoomObject):
    def __init__(self, coordinates=None, size="160x200", has_canopy=True):
        super().__init__("Ліжко", coordinates)
        self._size = size
        self._has_canopy = has_canopy

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def show(self):
        canopy = "з балдахіном" if self._has_canopy else "без балдахіна"
        print(f"Ліжко ({self._size}, {canopy}): координати = {self._coordinates}")


class Table(RoomObject):
    def __init__(self, coordinates=None, material="дуб", purpose="письмовий"):
        super().__init__("Стіл", coordinates)
        self._material = material
        self._purpose = purpose

    def get_material(self):
        return self._material

    def set_material(self, material):
        self._material = material

    def show(self):
        print(f"Стіл ({self._purpose}, {self._material}): координати = {self._coordinates}")


class Carpet(RoomObject):
    def __init__(self, coordinates=None, color="бежевий", pile="довгий ворс"):
        super().__init__("Килим", coordinates)
        self._color = color
        self._pile = pile

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def show(self):
        print(f"Килим ({self._color}, {self._pile}): координати = {self._coordinates}")


class Sofa(RoomObject):
    def __init__(self, coordinates=None, seats=3, color="сірий"):
        super().__init__("Диван", coordinates)
        self._seats = seats
        self._color = color

    def get_seats(self):
        return self._seats

    def set_seats(self, seats):
        self._seats = seats

    def show(self):
        print(f"Диван ({self._seats}-місний, {self._color}): координати = {self._coordinates}")


class Bookshelf(RoomObject):
    def __init__(self, coordinates=None, shelves=5):
        super().__init__("Книжкова шафа", coordinates)
        self._shelves = shelves

    def get_shelves(self):
        return self._shelves

    def set_shelves(self, shelves):
        self._shelves = shelves

    def show(self):
        print(f"Книжкова шафа ({self._shelves} полиць): координати = {self._coordinates}")


class Room:
    """Кімната, що містить колекцію предметів."""

    def __init__(self, name="Кімната моєї мрії", width=6, length=8):
        self._name = name
        self._width = width
        self._length = length
        self._items = []
        print(f"[+] Створено кімнату «{self._name}» ({width}x{length} м)")

    def __del__(self):
        print(f"[-] Кімнату «{self._name}» знищено")

    # ---- функції доступу ----
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_items(self):
        return list(self._items)

    def get_size(self):
        return self._width, self._length

    # ---- додавання / видалення ----
    def add_item(self, item):
        if not isinstance(item, RoomObject):
            raise TypeError("До кімнати можна додати лише об'єкт RoomObject")
        self._items.append(item)
        print(f"Додано до кімнати: {item.get_name()}")

    def remove_item(self, name):
        """Видалити перший предмет із заданою назвою. Повертає True/False."""
        for item in self._items:
            if item.get_name() == name:
                self._items.remove(item)
                print(f"Видалено з кімнати: {name}")
                return True
        print(f"Предмет «{name}» у кімнаті не знайдено")
        return False

    # ---- перестановка ----
    def rearrangement(self, new_positions=None, dx=0, dy=0):
        """
        Змінює координати об'єктів.
        new_positions — словник {назва: новий список координат};
        dx, dy — загальний зсув усіх предметів, яких немає у словнику.
        """
        new_positions = new_positions or {}
        for item in self._items:
            if item.get_name() in new_positions:
                item.set_coordinates(new_positions[item.get_name()])
            elif dx or dy:
                item.move(dx, dy)
        print("Перестановку виконано.")

    # ---- виведення ----
    def show(self):
        print(f"\n=== {self._name} ({self._width}x{self._length} м) ===")
        if not self._items:
            print("(кімната порожня)")
        for item in self._items:
            item.show()
        print("=" * 40 + "\n")


def main():
    room = Room("Кімната моєї мрії", 6, 8)

    bed = Bed([(0, 0), (2, 0), (2, 2), (0, 2)], size="180x200")
    table = Table([(4, 0), (6, 0), (6, 1), (4, 1)], material="дуб")
    carpet = Carpet([(1, 3), (5, 3), (5, 7), (1, 7)], color="смарагдовий")
    sofa = Sofa([(0, 6), (3, 6), (3, 7), (0, 7)], seats=3, color="бірюзовий")

    room.add_item(bed)
    room.add_item(table)
    room.add_item(carpet)
    room.add_item(sofa)
    room.show()

    print("--- Додаємо книжкову шафу ---")
    room.add_item(Bookshelf([(5, 6), (6, 6), (6, 8), (5, 8)], shelves=6))
    room.show()

    print("--- Перестановка: стіл і диван у нові місця, решта зсувається на (1, 1) ---")
    room.rearrangement(
        new_positions={
            "Стіл": [(3, 0), (5, 0), (5, 1), (3, 1)],
            "Диван": [(0, 4), (3, 4), (3, 5), (0, 5)],
        },
        dx=1,
        dy=1,
    )
    room.show()

    print("--- Видаляємо килим ---")
    room.remove_item("Килим")
    room.remove_item("Торшер")  # такого предмета немає
    room.show()

    # демонстрація функцій доступу
    print("Матеріал столу:", table.get_material())
    table.set_material("скло")
    print("Новий матеріал столу:", table.get_material())
    print("Координати ліжка:", bed.get_coordinates())

    print("\n--- Кінець програми ---")


if __name__ == "__main__":
    main()