import pytest
from praktikum.database import Database
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestDatabase:

    def test_database_initialization(self):
        db = Database()
        
        # Проверяем булки
        buns = db.available_buns()
        assert len(buns) == 3
        bun_names = [bun.get_name() for bun in buns]
        assert "black bun" in bun_names
        assert "white bun" in bun_names
        assert "red bun" in bun_names
        
        # Проверяем ингредиенты
        ingredients = db.available_ingredients()
        assert len(ingredients) == 6
        
        # Проверяем типы ингредиентов
        sauce_count = sum(1 for ing in ingredients if ing.get_type() == INGREDIENT_TYPE_SAUCE)
        filling_count = sum(1 for ing in ingredients if ing.get_type() == INGREDIENT_TYPE_FILLING)
        assert sauce_count == 3
        assert filling_count == 3

    def test_available_buns_returns_list(self):
        db = Database()
        buns = db.available_buns()
        assert isinstance(buns, list)
        assert len(buns) > 0

    def test_available_ingredients_returns_list(self):
        db = Database()
        ingredients = db.available_ingredients()
        assert isinstance(ingredients, list)
        assert len(ingredients) > 0