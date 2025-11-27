import pytest
from praktikum.bun import Bun

class TestBun:
    
    def test_bun_creation(self):
        bun = Bun("black bun", 100)
        assert bun.get_name() == "black bun"
        assert bun.get_price() == 100
    
    @pytest.mark.parametrize("name,price", [
        ("white bun", 200),
        ("red bun", 300),
        ("", 0),
        ("special bun", 999.99)
    ])
    def test_bun_get_name_and_price(self, name, price):
        bun = Bun(name, price)
        assert bun.get_name() == name
        assert bun.get_price() == price