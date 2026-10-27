from abc import ABC, abstractmethod
from typing import Any


class ProductsString(str):
    """Строка со списком товаров, поддерживающая подсчет товаров через len()."""

    product_count: int

    def __new__(
        cls,
        value: str,
        product_count: int,
    ) -> "ProductsString":
        obj = str.__new__(cls, value)
        obj.product_count = product_count
        return obj

    def __len__(self) -> int:
        """Возвращает количество товаров."""

        return self.product_count


class BaseProduct(ABC):
    """Абстрактный базовый класс для товаров."""

    @abstractmethod
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        if quantity == 0:
            raise ValueError(
                "Товар с нулевым количеством не может быть добавлен"
            )

        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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

    def __add__(self, other: "BaseProduct") -> float:
        """Возвращает общую стоимость запасов двух товаров."""

        if type(self) is not type(other):
            raise TypeError(
                "Нельзя складывать товары разных типов"
            )

        return (
            self.price * self.quantity
            + other.price * other.quantity
        )


class CreationInfoMixin:
    """Миксин для вывода информации о созданном объекте."""

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        arguments = [repr(argument) for argument in args]
        arguments.extend(
            f"{key}={value!r}"
            for key, value in kwargs.items()
        )

        print(
            f"{self.__class__.__name__}"
            f"({', '.join(arguments)})"
        )


class Product(CreationInfoMixin, BaseProduct):
    """Класс для представления товара."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        super().__init__(
            name,
            description,
            price,
            quantity,
        )

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """Создает новый товар из словаря."""

        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"],
        )

    def __str__(self) -> str:
        """Возвращает строковое представление товара."""

        return (
            f"{self.name}, {self.price} руб. "
            f"Остаток: {self.quantity} шт."
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

        return ProductsString(
            products_string,
            len(self.__products),
        )

    def middle_price(self) -> float:
        """Возвращает среднюю цену товаров категории."""

        try:
            total_price = sum(
                product.price
                for product in self.__products
            )
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0

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
