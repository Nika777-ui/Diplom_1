import pytest
from unittest.mock import Mock, patch
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:

    # Тесты для set_buns
    def test_set_buns(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        
        burger.set_buns(mock_bun)
        
        assert burger.bun == mock_bun

    # Тесты для add_ingredient
    def test_add_ingredient(self):
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        
        burger.add_ingredient(mock_ingredient)
        
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    # Тесты для remove_ingredient
    def test_remove_ingredient(self):
        burger = Burger()
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.remove_ingredient(0)
        
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient2

    # Тесты для move_ingredient
    @pytest.mark.parametrize("initial_index, new_index, expected_order", [
        (0, 1, [1, 0, 2]),
        (2, 0, [2, 0, 1]),
        (1, 1, [0, 1, 2])
    ])
    def test_move_ingredient(self, initial_index, new_index, expected_order):
        burger = Burger()
        mock_ingredients = [Mock(spec=Ingredient) for _ in range(3)]
        
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)
        
        burger.move_ingredient(initial_index, new_index)
        
        expected_ingredients = [mock_ingredients[i] for i in expected_order]
        assert burger.ingredients == expected_ingredients

    # Тесты для get_price
    @pytest.mark.parametrize("bun_price, ingredient_prices, expected_total", [
        (100, [50, 75], 325),  # 100*2 + 50 + 75
        (200, [], 400),        # 200*2 + 0
        (50, [10, 20, 30], 160)  # 50*2 + 10 + 20 + 30
    ])
    def test_get_price(self, bun_price, ingredient_prices, expected_total):
        burger = Burger()
        
        # Мок булочки
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        # Мок ингредиентов
        for price in ingredient_prices:
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)
        
        assert burger.get_price() == expected_total

    # Тесты для get_receipt
    def test_get_receipt_with_ingredients(self):
        burger = Burger()
        
        # Мок булочки
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = "black bun"
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)
        
        # Мок ингредиентов
        mock_sauce = Mock(spec=Ingredient)
        mock_sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_sauce.get_name.return_value = "hot sauce"
        mock_sauce.get_price.return_value = 50
        
        mock_filling = Mock(spec=Ingredient)
        mock_filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        mock_filling.get_name.return_value = "cutlet"
        mock_filling.get_price.return_value = 75
        
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        
        receipt = burger.get_receipt()
        
        expected_lines = [
            "(==== black bun ====)",
            "= sauce hot sauce =",
            "= filling cutlet =", 
            "(==== black bun ====)",
            "Price: 325"
        ]
        
        for line in expected_lines:
            assert line in receipt

    def test_get_receipt_empty_burger(self):
        burger = Burger()
        
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 200
        burger.set_buns(mock_bun)
        
        receipt = burger.get_receipt()
        
        expected_lines = [
            "(==== white bun ====)",
            "(==== white bun ====)",
            "Price: 400"
        ]
        
        for line in expected_lines:
            assert line in receipt

    # Тест на удаление несуществующего ингредиента
    def test_remove_ingredient_invalid_index_raises_error(self):
        burger = Burger()
        
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    # Тест на перемещение несуществующего ингредиента
    def test_move_ingredient_invalid_index_raises_error(self):
        burger = Burger()
        
        with pytest.raises(IndexError):
            burger.move_ingredient(0, 1)