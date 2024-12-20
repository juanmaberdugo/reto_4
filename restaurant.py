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
            print("El monto no puede ser negativo.")
        self.__monto = monto

    def get_monto(self):
        return self.__monto

    def pagar_con_tarjeta(self, numero, cvv):
        if len(numero) < 4:
            print("El número de tarjeta debe tener al menos 4 dígitos.")
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