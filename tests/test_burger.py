import pytest
from unittest.mock import Mock, patch
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING

# Импортируем тестовые данные из отдельного модуля
from tests.data.burger_test_data import (
    TEST_BUNS,
    TEST_INGREDIENTS,
    PRICE_TEST_DATA,
    MOVE_INGREDIENT_TEST_DATA,
    RECEIPT_TEST_DATA
)


class TestBurger:
    """Тесты для класса Burger"""
    
    # ===== Тесты для set_buns =====
    
    def test_set_buns(self):
        """Проверяем установку булки в бургер"""
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        
        burger.set_buns(mock_bun)
        
        assert burger.bun == mock_bun
    
    # ===== Тесты для add_ingredient =====
    
    def test_add_ingredient(self):
        """Проверяем добавление ингредиента в бургер"""
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        
        burger.add_ingredient(mock_ingredient)
        
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient
    
    # ===== Тесты для remove_ingredient =====
    
    def test_remove_ingredient(self):
        """Проверяем удаление ингредиента из бургера"""
        burger = Burger()
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.remove_ingredient(0)
        
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient2
    
    def test_remove_ingredient_invalid_index_raises_error(self):
        """Проверяем ошибку при удалении несуществующего ингредиента"""
        burger = Burger()
        
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)
    
    # ===== Тесты для move_ingredient =====
    
    @pytest.mark.parametrize("initial_index, new_index, expected_order", 
                             MOVE_INGREDIENT_TEST_DATA)
    def test_move_ingredient(self, initial_index, new_index, expected_order):
        """Проверяем перемещение ингредиента в бургере"""
        burger = Burger()
        
        # Создаем 3 мока ингредиентов
        mock_ingredients = [Mock(spec=Ingredient) for _ in range(3)]
        
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)
        
        burger.move_ingredient(initial_index, new_index)
        
        # Проверяем новый порядок
        expected_ingredients = [mock_ingredients[i] for i in expected_order]
        assert burger.ingredients == expected_ingredients
    
    def test_move_ingredient_invalid_index_raises_error(self):
        """Проверяем ошибку при перемещении несуществующего ингредиента"""
        burger = Burger()
        
        with pytest.raises(IndexError):
            burger.move_ingredient(0, 1)
    
    # ===== Тесты для get_price =====
    
    @pytest.mark.parametrize("bun_price, ing_price1, ing_price2, expected_total", 
                             PRICE_TEST_DATA)
    def test_get_price(self, bun_price, ing_price1, ing_price2, expected_total):
        """Проверяем расчет цены бургера с разными ценами"""
        burger = Burger()
        
        # Мок булочки
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        # Мок ингредиентов
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient1.get_price.return_value = ing_price1
        
        mock_ingredient2 = Mock(spec=Ingredient)
        mock_ingredient2.get_price.return_value = ing_price2
        
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        
        assert burger.get_price() == expected_total
    
    def test_get_price_no_bun_raises_error(self):
        """Проверяем что цена без булки вызывает ошибку"""
        burger = Burger()
        
        # Не устанавливаем булку (burger.bun = None)
        mock_ingredient = Mock(spec=Ingredient)
        burger.add_ingredient(mock_ingredient)
        
        # Метод get_price() не обрабатывает bun = None
        # Должен вызывать AttributeError
        with pytest.raises(AttributeError):
            burger.get_price()
    
    def test_get_price_no_ingredients(self):
        """Проверяем расчет цены бургера без ингредиентов"""
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = 250
        burger.set_buns(mock_bun)
        
        assert burger.get_price() == 500  # 2 * 250
    
    # ===== Тесты для get_receipt =====
    
    def test_get_receipt_with_ingredients(self):
        """Проверяем формирование чека с ингредиентами"""
        burger = Burger()
        
        # Мок булочки из тестовых данных
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = TEST_BUNS[0]["name"]
        mock_bun.get_price.return_value = TEST_BUNS[0]["price"]
        burger.set_buns(mock_bun)
        
        # Мок ингредиентов из тестовых данных
        mock_sauce = Mock(spec=Ingredient)
        mock_sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_sauce.get_name.return_value = TEST_INGREDIENTS[0]["name"]
        mock_sauce.get_price.return_value = TEST_INGREDIENTS[0]["price"]
        
        mock_filling = Mock(spec=Ingredient)
        mock_filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        mock_filling.get_name.return_value = TEST_INGREDIENTS[2]["name"]
        mock_filling.get_price.return_value = TEST_INGREDIENTS[2]["price"]
        
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        
        receipt = burger.get_receipt()
        
        # Проверяем ключевые элементы чека
        expected_total = 2 * TEST_BUNS[0]["price"] + TEST_INGREDIENTS[0]["price"] + TEST_INGREDIENTS[2]["price"]
        
        assert f"(==== {TEST_BUNS[0]['name']} ====)" in receipt
        assert f"= sauce {TEST_INGREDIENTS[0]['name']} =" in receipt
        assert f"= filling {TEST_INGREDIENTS[2]['name']} =" in receipt
        assert f"Price: {expected_total}" in receipt
    
    def test_get_receipt_empty_burger(self):
        """Проверяем формирование чека без ингредиентов"""
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = TEST_BUNS[1]["name"]
        mock_bun.get_price.return_value = TEST_BUNS[1]["price"]
        burger.set_buns(mock_bun)
        
        receipt = burger.get_receipt()
        
        expected_total = 2 * TEST_BUNS[1]["price"]
        
        assert f"(==== {TEST_BUNS[1]['name']} ====)" in receipt
        assert f"Price: {expected_total}" in receipt
        # Проверяем что ингредиенты не упоминаются
        assert "= sauce" not in receipt
        assert "= filling" not in receipt
    
    @pytest.mark.parametrize("test_case", RECEIPT_TEST_DATA)
    def test_get_receipt_parametrized(self, test_case):
        """Параметризованный тест формирования чека"""
        burger = Burger()
        
        # Мок булочки
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = test_case["bun_name"]
        mock_bun.get_price.return_value = test_case["bun_price"]
        burger.set_buns(mock_bun)
        
        # Мок ингредиентов
        for name, price, ing_type in test_case["ingredients"]:
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_name.return_value = name
            mock_ingredient.get_price.return_value = price
            mock_ingredient.get_type.return_value = ing_type
            burger.add_ingredient(mock_ingredient)
        
        receipt = burger.get_receipt()
        
        # Проверяем основные элементы
        assert f"(==== {test_case['bun_name']} ====)" in receipt
        assert f"Price: {test_case['expected_total']}" in receipt
        
        # Проверяем каждый ингредиент
        for name, price, ing_type in test_case["ingredients"]:
            assert f"= {ing_type.lower()} {name} =" in receipt
    
    # ===== Дополнительный тест для полного покрытия =====
    
    def test_move_ingredient_full_coverage(self):
        """Тест для полного покрытия метода move_ingredient"""
        burger = Burger()
        
        # Создаем два ингредиента
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        # Перемещаем - это выполнит строку self.ingredients.insert(new_index, self.ingredients.pop(index))
        burger.move_ingredient(0, 1)
        
        # Проверяем что переместилось
        assert burger.ingredients == [ingredient2, ingredient1]
        
        # Перемещаем обратно
        burger.move_ingredient(1, 0)
        assert burger.ingredients == [ingredient1, ingredient2]