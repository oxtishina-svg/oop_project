class Product:
    """Класс для представления товара."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """Создает новый товар из словаря."""

        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"],
        )

    @property
    def price(self) -> float:
        """Возвращает цену товара."""

        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Устанавливает новую цену товара."""

        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        self.__price = new_price

    def __str__(self) -> str:
        """Возвращает строковое представление товара."""

        return (
            f"{self.name}, {self.price} руб. "
            f"Остаток: {self.quantity} шт."
        )

    def __add__(self, other: "Product") -> float:
        """Возвращает общую стоимость запасов двух товаров."""

        if type(self) is not type(other):
            raise TypeError(
                "Нельзя складывать товары разных типов"
            )

        return (
            self.price * self.quantity
            + other.price * other.quantity
        )


class Smartphone(Product):
    """Класс для представления смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(
            name,
            description,
            price,
            quantity,
        )
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(
            name,
            description,
            price,
            quantity,
        )
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[Product],
    ) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию."""

        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только товары класса Product "
                "или его наследников"
            )

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку со всеми товарами категории."""

        products_string = ""

        for product in self.__products:
            products_string += f"{product}\n"

        return products_string

    def __str__(self) -> str:
        """Возвращает строковое представление категории."""

        total_quantity = sum(
            product.quantity
            for product in self.__products
        )

        return (
            f"{self.name}, количество продуктов: "
            f"{total_quantity} шт."
        )
