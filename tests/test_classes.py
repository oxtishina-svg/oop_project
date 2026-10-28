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
        "Смартфоны, как средство не только коммуникации",
        [product, second_product],
    )

    assert category.name == "Смартфоны"
    assert (
        category.description
        == "Смартфоны, как средство не только коммуникации"
    )
    assert category.products == [product, second_product]


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
