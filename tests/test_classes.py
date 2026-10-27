import pytest

from src.classes import Category, Product


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


def test_product_initialization(product: Product) -> None:
    """Проверяет корректность инициализации Product."""

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


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
