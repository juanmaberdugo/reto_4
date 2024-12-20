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