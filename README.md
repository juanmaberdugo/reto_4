# reto_4

## Primer ejercicio
Se creo la clase Shape y se consigio implementar los metodos compute_area() y compute_perimeter() de distinta manera tanto en la clase Triangle como en la clase rectangle, usando polimorfismo.

```python
class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def compute_distance(self, point: "Point") -> float:
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5


class Line:
    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point

    def compute_length(self) -> float:
        return self.start_point.compute_distance(self.end_point)


class Shape:
    def __init__(self, is_regular: bool = False):
        self.is_regular = is_regular
        self.vertices = []
        self.edges = []
        self.inner_angles = [] 

    def compute_area(self):
        ...

    def compute_perimeter(self):
        ...

class Rectangle(Shape):
    def __init__(self, **kwargs):
        if "center" in kwargs:
            center = kwargs["center"]
            width = kwargs["width"]
            height = kwargs["height"]
            x = center.x - width / 2
            y = center.y - height / 2
        elif "bottom_left" in kwargs and "upper_right" in kwargs:
            bottom_left = kwargs["bottom_left"]
            upper_right = kwargs["upper_right"]
            x = bottom_left.x
            y = bottom_left.y
            width = upper_right.x - bottom_left.x
            height = upper_right.y - bottom_left.y
        else:
            x = kwargs["x"]
            y = kwargs["y"]
            width = kwargs["width"]
            height = kwargs["height"]

        self.bottom_left = Point(x, y)
        self.upper_right = Point(x + width, y + height)
        self.width = width
        self.height = height

    def compute_perimeter(self):
        return 2 * (self.width + self.height)

    def compute_area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side_length: float, **kwargs):
        kwargs["width"] = side_length
        kwargs["height"] = side_length
        super().__init__(**kwargs)

class Triangle(Shape):
    def __init__(self, vertices: list[Point]):
        super().__init__(is_regular=False)
        if len(vertices) != 3:
            print("Un triángulo debe tener exactamente 3 vértices.")
        self.vertices = vertices
        self.edges = []
        self._build_edges()

    def _build_edges(self):
        first_edge = Line(self.vertices[0], self.vertices[1])
        second_edge = Line(self.vertices[1], self.vertices[2])
        third_edge = Line(self.vertices[2], self.vertices[0])
        self.edges.append(first_edge)
        self.edges.append(second_edge)
        self.edges.append(third_edge)

    def compute_perimeter(self) -> float:
        total_length = 0
        for edge in self.edges:
            total_length += edge.compute_length()
        return total_length

    def compute_area(self) -> float:
        a = self.edges[0].compute_length()
        b = self.edges[1].compute_length()
        c = self.edges[2].compute_length()
        s = self.compute_perimeter() / 2
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        return area


class Equilateral(Triangle):
    def __init__(self, vertices: list[Point]):
        super().__init__(vertices)
        first_length = self.edges[0].compute_length()
        for edge in self.edges:
            if abs(edge.compute_length() - first_length) > 1e-9:
                print("Todos los lados de un triangulo equilatero deben ser iguales.")
        self.is_regular = True


class Isosceles(Triangle):
    def __init__(self, vertices: list[Point]):
        super().__init__(vertices)
        lengths = [edge.compute_length() for edge in self.edges]
        unique_lengths = set(lengths)
        if len(unique_lengths) > 2:
            print("Un triangulo isósceles debe tener al menos dos lados iguales.")


class Scalene(Triangle):
    def __init__(self, vertices: list[Point]):
        super().__init__(vertices)
        lengths = [edge.compute_length() for edge in self.edges]
        unique_lengths = set(lengths)
        if len(unique_lengths) != 3:
            print("Un triangulo escaleno debe tener todos los lados de diferente longitud.")


class TriRectangle(Triangle):
    def __init__(self, vertices: list[Point]):
        super().__init__(vertices)
        lengths = sorted([edge.compute_length() for edge in self.edges])
        a, b, c = lengths
        if abs(a**2 + b**2 - c**2) > 1e-9:
            print("Un triangulo rectángulo debe cumplir el teorema de Pitagoras.")


bottom_left = Point(0, 0)
rect = Rectangle(x=0, y=0, width=10, height=5)
print(f"Area del rectángulo: {rect.compute_area()}")
print(f"Perimetro del rectángulo: {rect.compute_perimeter()}")

square = Square(x=0, y=0, side_length=10)
print(f"Area del cuadrado: {square.compute_area()}")
print(f"Perimetro del cuadrado: {square.compute_perimeter()}")

triangle_vertices = [Point(0, 0), Point(4, 0), Point(0, 3)]
triangle = Triangle(triangle_vertices)
print(f"Area del triangulo: {triangle.compute_area()}")
print(f"Perimetro del triangulo: {triangle.compute_perimeter()}")

trirectangle_vertices = [Point(0, 0), Point(3, 0), Point(0, 4)]
trirectangle = TriRectangle(trirectangle_vertices)
print(f"Area del triangulo rectángulo: {trirectangle.compute_area()}")
print(f"Perimetro del triangulo rectangulo: {trirectangle.compute_perimeter()}")
```

## Segundo ejercicio

Se creo la clase PayThem haciendo uso del encapsulamiento, en las subclases de MenuItem se añadieron getters y setters, y finalment se añadio la funcionalidad en orden de hacer un descuento si hay productos en MainCourse.

```python
class MenuItem:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def calculate_price(self, quantity=1):
        return self.price * quantity

    def get_details(self):
        return f"{self.name}: COP {self.price}"


class Beverage(MenuItem):
    def __init__(self, name, price, size, is_carbonated):
        super().__init__(name, price, "Beverage")
        self.__size = size
        self.__is_carbonated = "Si" if is_carbonated else "No"

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size

    def get_is_carbonated(self):
        return self.__is_carbonated

    def set_is_carbonated(self, is_carbonated):
        self.__is_carbonated = "Sí" if is_carbonated else "No"

    def get_details(self):
        return (
            f"{super().get_details()}, Tamaño: {self.get_size()}ml, "
            f"Carbonatada: {self.get_is_carbonated()}"
        )


class Appetizer(MenuItem):
    def __init__(self, name, price, portion_size, has_sauces):
        super().__init__(name, price, "Appetizer")
        self.__portion_size = portion_size
        self.__has_sauces = "Si" if has_sauces else "No"

    def get_portion_size(self):
        return self.__portion_size

    def set_portion_size(self, portion_size):
        self.__portion_size = portion_size

    def get_has_sauces(self):
        return self.__has_sauces

    def set_has_sauces(self, has_sauces):
        self.__has_sauces = "Si" if has_sauces else "No"

    def get_details(self):
        return (
            f"{super().get_details()}, Porcion: {self.get_portion_size()}, "
            f"Con salsas: {self.get_has_sauces()}"
        )


class MainCourse(MenuItem):
    def __init__(self, name, price, origin, cooking_time):
        super().__init__(name, price, "MainCourse")
        self.__origin = origin
        self.__cooking_time = cooking_time

    def get_origin(self):
        return self.__origin

    def set_origin(self, origin):
        self.__origin = origin

    def get_cooking_time(self):
        return self.__cooking_time

    def set_cooking_time(self, cooking_time):
        self.__cooking_time = cooking_time

    def get_details(self):
        return (
            f"{super().get_details()}, Origen: {self.get_origin()}, "
            f"Tiempo de preparacion: {self.get_cooking_time()} min"
        )


class Order:
    def __init__(self):
        self.items = []
        self.has_main_course = False

    def add_item(self, menu_item, quantity=1):
        self.items.append((menu_item, quantity))
        if menu_item.category == "MainCourse":
            self.has_main_course = True

    def calculate_total(self):
        total = 0
        for item, quantity in self.items:
            if self.has_main_course and item.category == "Beverage":
                total += item.calculate_price(quantity) * 0.8
            else:
                total += item.calculate_price(quantity)
        return total

    def generate_bill(self, filename):
        with open(filename, "w") as file:
            file.write("Factura\n")
            file.write("==========\n")
            for item, quantity in self.items:
                file.write(
                    f"{item.get_details()} x{quantity}: COP {item.calculate_price(quantity)}\n"
                )
            file.write("==========\n")
            total = self.calculate_total()
            file.write(f"Total: COP {total}\n")
            file.write("==========\n")
            file.write("Gracias por su compra!\n")

    def get_order_details(self):
        receipt = "Detalles de la Orden:\n"
        for item, quantity in self.items:
            receipt += (
                f"{item.get_details()} x{quantity}: COP {item.calculate_price(quantity)}\n"
            )
        receipt += f"Total: COP {self.calculate_total()}"
        return receipt


class PayThem:
    def __init__(self):
        self.__monto = 0

    def set_monto(self, monto):
        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        self.__monto = monto

    def get_monto(self):
        return self.__monto

    def pagar_con_tarjeta(self, numero, cvv):
        if len(numero) < 4:
            raise ValueError("El número de tarjeta debe tener al menos 4 dígitos.")
        print(f"Pagando COP {self.__monto} con tarjeta {numero[-4:]}")

    def pagar_en_efectivo(self, monto_entregado):
        if monto_entregado < self.__monto:
            print(f"Fondos insuficientes. Faltan COP {self.__monto - monto_entregado} para completar el pago.")
        else:
            cambio = monto_entregado - self.__monto
            print(f"Pago realizado en efectivo. Cambio: COP {cambio}")


menu_items = [
    Beverage("Gaseosa", 2500.00, 500, True),
    Beverage("Café", 2000.00, 250, False),
    Beverage("Té Helado", 3000.00, 300, False),
    Appetizer("Papas Fritas", 4000.00, "Mediana", True),
    Appetizer("Nachos", 6000.00, "Grande", True),
    Appetizer("Alitas de Pollo", 8000.00, "Grande", True),
    MainCourse("Pasta Carbonara", 12000.00, "Italia", 15),
    MainCourse("Tacos al Pastor", 10000.00, "Mexico", 10),
    MainCourse("Pollo Asado", 15000.00, "Colombia", 20),
    MainCourse("Sushi", 20000.00, "Japon", 25),
]

order = Order()
order.add_item(menu_items[0], 2)  
order.add_item(menu_items[3], 1)  
order.add_item(menu_items[6], 1)  
order.add_item(menu_items[7], 2)  

print(order.get_order_details())

order.generate_bill("factura.txt")
print("Factura generada en el archivo 'factura.txt'.")


pago = PayThem()
pago.set_monto(order.calculate_total())
pago.pagar_con_tarjeta("1234567890123456", 123)
```
