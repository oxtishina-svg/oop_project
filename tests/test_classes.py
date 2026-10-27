from abc import ABC

import pytest

from src.classes import BaseProduct, Category, LawnGrass, Product, Smartphone


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Сбрасывает счетчики Category перед каждым тестом."""

    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product() -> Product:
    """Создает тестовый товар."""

    return Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, серый цвет, 200MP камера",
        180000.0,
        5,
    )


@pytest.fixture
def second_product() -> Product:
    """Создает второй тестовый товар."""

    return Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
    )


@pytest.fixture
def smartphone() -> Smartphone:
    """Создает тестовый смартфон."""

    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )


@pytest.fixture
def second_smartphone() -> Smartphone:
    """Создает второй тестовый смартфон."""

    return Smartphone(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
        90.0,
        "15",
        512,
        "Gray space",
    )


@pytest.fixture
def lawn_grass() -> LawnGrass:
    """Создает тестовую газонную траву."""

    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


def test_base_product_is_abstract() -> None:
    """Проверяет, что BaseProduct является абстрактным классом."""

    assert issubclass(BaseProduct, ABC)

    with pytest.raises(TypeError):
        BaseProduct(
            "Товар",
            "Описание",
            100.0,
            1,
        )


def test_product_initialization(product: Product) -> None:
    """Проверяет корректность инициализации Product."""

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_product_inherits_base_product(product: Product) -> None:
    """Проверяет наследование Product от BaseProduct."""

    assert isinstance(product, BaseProduct)


def test_smartphone_initialization(
    smartphone: Smartphone,
) -> None:
    """Проверяет корректность инициализации Smartphone."""

    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.price == 180000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_lawn_grass_initialization(
    lawn_grass: LawnGrass,
) -> None:
    """Проверяет корректность инициализации LawnGrass."""

    assert lawn_grass.name == "Газонная трава"
    assert lawn_grass.price == 500.0
    assert lawn_grass.quantity == 20
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7 дней"
    assert lawn_grass.color == "Зеленый"


def test_creation_info_mixin(capsys) -> None:
    """Проверяет вывод информации при создании Product."""

    Product(
        "Тестовый товар",
        "Описание",
        1000.0,
        3,
    )

    captured = capsys.readouterr()

    assert (
        "Product('Тестовый товар', 'Описание', 1000.0, 3)"
        in captured.out
    )


def test_category_initialization(
    product: Product,
    second_product: Product,
) -> None:
    """Проверяет корректность инициализации Category."""

    category = Category(
        "Смартфоны",
        "Описание категории",
        [product, second_product],
    )

    assert category.name == "Смартфоны"
    assert category.description == "Описание категории"
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_products(
    product: Product,
    second_product: Product,
) -> None:
    """Проверяет геттер списка товаров."""

    category = Category(
        "Смартфоны",
        "Описание категории",
        [product, second_product],
    )

    expected = (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
    )

    assert category.products == expected


def test_add_product(
    product: Product,
    second_product: Product,
) -> None:
    """Проверяет добавление товара в категорию."""

    category = Category(
        "Смартфоны",
        "Описание категории",
        [product],
    )

    category.add_product(second_product)

    assert Category.product_count == 2
    assert "Iphone 15" in category.products


def test_add_smartphone_to_category(
    product: Product,
    smartphone: Smartphone,
) -> None:
    """Проверяет добавление наследника Product в категорию."""

    category = Category(
        "Товары",
        "Описание категории",
        [product],
    )

    category.add_product(smartphone)

    assert Category.product_count == 2
    assert "Samsung Galaxy S23 Ultra" in category.products


def test_add_invalid_object_to_category(product: Product) -> None:
    """Проверяет запрет добавления постороннего объекта."""

    category = Category(
        "Товары",
        "Описание категории",
        [product],
    )

    with pytest.raises(TypeError):
        category.add_product("не товар")  # type: ignore[arg-type]


def test_category_count(
    product: Product,
    second_product: Product,
) -> None:
    """Проверяет подсчет количества категорий."""

    Category(
        "Смартфоны",
        "Описание категории",
        [product],
    )
    Category(
        "Ноутбуки",
        "Описание категории",
        [second_product],
    )

    assert Category.category_count == 2


def test_product_count(
    product: Product,
    second_product: Product,
) -> None:
    """Проверяет подсчет количества товаров."""

    Category(
        "Смартфоны",
        "Описание категории",
        [product, second_product],
    )

    assert Category.product_count == 2


def test_new_product() -> None:
    """Проверяет создание товара через classmethod."""

    product_data = {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14,
    }

    product = Product.new_product(product_data)

    assert product.name == "Xiaomi Redmi Note 11"
    assert product.description == "1024GB, Синий"
    assert product.price == 31000.0
    assert product.quantity == 14


def test_price_getter(product: Product) -> None:
    """Проверяет геттер цены."""

    assert product.price == 180000.0


def test_price_setter(product: Product) -> None:
    """Проверяет изменение цены."""

    product.price = 190000.0

    assert product.price == 190000.0


def test_price_setter_invalid(
    product: Product,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Проверяет запрет нулевой и отрицательной цены."""

    product.price = 0

    captured = capsys.readouterr()

    assert product.price == 180000.0
    assert (
        "Цена не должна быть нулевая или отрицательная"
        in captured.out
    )


def test_product_str(product: Product) -> None:
    """Проверяет строковое представление товара."""

    assert str(product) == (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. "
        "Остаток: 5 шт."
    )


def test_category_str(
    product: Product,
    second_product: Product,
) -> None:
    """Проверяет строковое представление категории."""

    category = Category(
        "Смартфоны",
        "Описание категории",
        [product, second_product],
    )

    assert str(category) == (
        "Смартфоны, количество продуктов: 13 шт."
    )


def test_product_add(
    product: Product,
    second_product: Product,
) -> None:
    """Проверяет сложение двух Product."""

    result = product + second_product

    assert result == 2580000.0


def test_smartphone_add(
    smartphone: Smartphone,
    second_smartphone: Smartphone,
) -> None:
    """Проверяет сложение двух Smartphone."""

    result = smartphone + second_smartphone

    assert result == 2580000.0


def test_add_different_product_types(
    smartphone: Smartphone,
    lawn_grass: LawnGrass,
) -> None:
    """Проверяет запрет сложения товаров разных классов."""

    with pytest.raises(TypeError):
        smartphone + lawn_grass
