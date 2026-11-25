class RoomObject:
    _next_id = 1

    def __init__(self, name="Предмет", coordinates=None, obj_id=None):
        self._id = obj_id if obj_id is not None else RoomObject._next_id
        if obj_id is None:
            RoomObject._next_id += 1
        self._name = name
        self._coordinates = []
        if coordinates is not None:
            self.set_coordinates(coordinates)
        print(f"[+] Створено: {self._name} (id={self._id})")

    def __del__(self):
        print(f"[-] Знищено: {self._name} (id={self._id})")

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Назва предмета має бути непорожнім рядком.")
        self._name = name.strip()

    def get_coordinates(self):
        return list(self._coordinates)

    def set_coordinates(self, coordinates):
        if not isinstance(coordinates, (list, tuple)) or len(coordinates) == 0:
            raise ValueError("Координати мають бути непорожнім списком точок (x, y).")

        validated = []
        for point in coordinates:
            if (
                not isinstance(point, (list, tuple))
                or len(point) != 2
                or isinstance(point[0], bool)
                or isinstance(point[1], bool)
                or not isinstance(point[0], (int, float))
                or not isinstance(point[1], (int, float))
            ):
                raise ValueError(f"Некоректна точка координат: {point}")
            validated.append((point[0], point[1]))

        self._coordinates = validated

    def move(self, dx, dy):
        if (
            isinstance(dx, bool)
            or isinstance(dy, bool)
            or not isinstance(dx, (int, float))
            or not isinstance(dy, (int, float))
        ):
            raise ValueError("Зсув dx та dy має бути числовим.")
        self._coordinates = [(x + dx, y + dy) for (x, y) in self._coordinates]

    def show(self):
        print(f"{self._name} [id={self._id}]: координати = {self._coordinates}")


class Bed(RoomObject):
    def __init__(self, coordinates=None, size="160x200", has_canopy=True, obj_id=None):
        super().__init__("Ліжко", coordinates, obj_id=obj_id)
        self._size = size
        self._has_canopy = bool(has_canopy)

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def get_has_canopy(self):
        return self._has_canopy

    def set_has_canopy(self, has_canopy):
        self._has_canopy = bool(has_canopy)

    def show(self):
        canopy = "з балдахіном" if self._has_canopy else "без балдахіна"
        print(f"Ліжко [id={self._id}] ({self._size}, {canopy}): координати = {self._coordinates}")


class Table(RoomObject):
    def __init__(self, coordinates=None, material="дуб", purpose="письмовий", obj_id=None):
        super().__init__("Стіл", coordinates, obj_id=obj_id)
        self._material = material
        self._purpose = purpose

    def get_material(self):
        return self._material

    def set_material(self, material):
        self._material = material

    def get_purpose(self):
        return self._purpose

    def set_purpose(self, purpose):
        self._purpose = purpose

    def show(self):
        print(f"Стіл [id={self._id}] ({self._purpose}, {self._material}): координати = {self._coordinates}")


class Carpet(RoomObject):
    def __init__(self, coordinates=None, color="бежевий", pile="довгий ворс", obj_id=None):
        super().__init__("Килим", coordinates, obj_id=obj_id)
        self._color = color
        self._pile = pile

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def get_pile(self):
        return self._pile

    def set_pile(self, pile):
        self._pile = pile

    def show(self):
        print(f"Килим [id={self._id}] ({self._color}, {self._pile}): координати = {self._coordinates}")


class Sofa(RoomObject):
    def __init__(self, coordinates=None, seats=3, color="сірий", obj_id=None):
        super().__init__("Диван", coordinates, obj_id=obj_id)
        self._seats = seats
        self._color = color

    def get_seats(self):
        return self._seats

    def set_seats(self, seats):
        self._seats = seats

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def show(self):
        print(f"Диван [id={self._id}] ({self._seats}-місний, {self._color}): координати = {self._coordinates}")


class Bookshelf(RoomObject):
    def __init__(self, coordinates=None, shelves=5, obj_id=None):
        super().__init__("Книжкова шафа", coordinates, obj_id=obj_id)
        self._shelves = shelves

    def get_shelves(self):
        return self._shelves

    def set_shelves(self, shelves):
        self._shelves = shelves

    def show(self):
        print(f"Книжкова шафа [id={self._id}] ({self._shelves} полиць): координати = {self._coordinates}")


class Room:
    def __init__(self, name="Кімната моєї мрії", width=6, length=8):
        if width <= 0 or length <= 0:
            raise ValueError("Розміри кімнати мають бути додатними.")
        self._name = name
        self._width = width
        self._length = length
        self._items = []
        print(f"[+] Створено кімнату «{self._name}» ({width}x{length} м)")

    def __del__(self):
        print(f"[-] Кімнату «{self._name}» знищено")

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_items(self):
        return list(self._items)

    def get_size(self):
        return self._width, self._length

    def _validate_in_bounds(self, coordinates):
        for x, y in coordinates:
            if x < 0 or x > self._width or y < 0 or y > self._length:
                raise ValueError(
                    f"Координати ({x}, {y}) виходять за межі кімнати {self._width}x{self._length} м."
                )

    def add_item(self, item):
        if not isinstance(item, RoomObject):
            raise TypeError("До кімнати можна додати лише об'єкт RoomObject")
        if any(existing.get_id() == item.get_id() for existing in self._items):
            raise ValueError(f"Предмет з id={item.get_id()} уже є в кімнаті.")
        self._validate_in_bounds(item.get_coordinates())
        self._items.append(item)
        print(f"Додано до кімнати: {item.get_name()} (id={item.get_id()})")

    def remove_item(self, target):
        if isinstance(target, RoomObject):
            if target in self._items:
                self._items.remove(target)
                print(f"Видалено з кімнати: {target.get_name()} (id={target.get_id()})")
                return True
            print(f"Об'єкт {target.get_name()} (id={target.get_id()}) у кімнаті не знайдено")
            return False

        if isinstance(target, int) and not isinstance(target, bool):
            if 0 <= target < len(self._items):
                removed = self._items.pop(target)
                print(f"Видалено з кімнати: {removed.get_name()} (id={removed.get_id()})")
                return True
            print(f"Предмет за індексом {target} не знайдено")
            return False

        if isinstance(target, str):
            for item in self._items:
                if item.get_name() == target:
                    self._items.remove(item)
                    print(f"Видалено з кімнати: {target} (id={item.get_id()})")
                    return True
            print(f"Предмет «{target}» у кімнаті не знайдено")
            return False

        raise TypeError("Очікується RoomObject, int (індекс) або str (назва).")

    def rearrange(self, new_positions=None, dx=0, dy=0):
        new_positions = new_positions or {}
        planned_coords = {}

        for item in self._items:
            if item.get_id() in new_positions:
                coords = new_positions[item.get_id()]
            elif item in new_positions:
                coords = new_positions[item]
            elif item.get_name() in new_positions:
                coords = new_positions[item.get_name()]
            elif dx or dy:
                coords = [(x + dx, y + dy) for (x, y) in item.get_coordinates()]
            else:
                coords = item.get_coordinates()

            self._validate_in_bounds(coords)
            planned_coords[item.get_id()] = coords

        for item in self._items:
            item.set_coordinates(planned_coords[item.get_id()])

        print("Перестановку виконано.")

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
    room.add_item(Bookshelf([(4, 5), (5, 5), (5, 7), (4, 7)], shelves=6))
    room.show()

    print("--- Перестановка: стіл і диван у нові місця, решта зсувається на (1, 1) ---")
    room.rearrange(
        new_positions={
            table.get_id(): [(3, 0), (5, 0), (5, 1), (3, 1)],
            sofa.get_id(): [(0, 4), (3, 4), (3, 5), (0, 5)],
        },
        dx=1,
        dy=1,
    )
    room.show()

    print("--- Видаляємо килим ---")
    room.remove_item(carpet)
    del carpet
    room.remove_item("Торшер")
    room.show()

    print("Матеріал столу:", table.get_material())
    table.set_material("скло")
    print("Новий матеріал столу:", table.get_material())
    print("Призначення столу:", table.get_purpose())
    print("Ворс килима:", Carpet(pile="короткий ворс").get_pile())
    print("Колір дивана:", sofa.get_color())
    print("Наявність балдахіна:", bed.get_has_canopy())
    print("Координати ліжка:", bed.get_coordinates())

    print("\n--- Кінець програми ---")


if __name__ == "__main__":
    main()
