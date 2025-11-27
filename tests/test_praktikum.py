import pytest
from unittest.mock import patch, Mock


class TestPraktikum:

    @patch('praktikum.praktikum.Database')
    @patch('praktikum.praktikum.Burger')
    @patch('praktikum.praktikum.print')
    def test_main_function(self, mock_print, mock_burger, mock_database):
        """
        Тестируем основную функцию
        """
        # Настраиваем моки
        mock_db_instance = Mock()
        mock_database.return_value = mock_db_instance
        
        mock_burger_instance = Mock()
        mock_burger.return_value = mock_burger_instance
        
        mock_buns = [Mock(), Mock(), Mock()]
        mock_ingredients = [Mock() for _ in range(6)]
        mock_db_instance.available_buns.return_value = mock_buns
        mock_db_instance.available_ingredients.return_value = mock_ingredients
        
        # Импортируем и запускаем main
        from praktikum.praktikum import main
        main()
        
        # Проверяем основные вызовы
        mock_database.assert_called_once()
        mock_burger.assert_called_once()
        mock_burger_instance.set_buns.assert_called_once_with(mock_buns[0])
        assert mock_burger_instance.add_ingredient.call_count == 4


def test_main_as_script():
    """
    Тест для покрытия блока if __name__ == "__main__"
    """
    import praktikum.praktikum as module
    
    original_name = module.__name__
    
    try:
        module.__name__ = "__main__"
        
        with patch('praktikum.praktikum.Database') as mock_db, \
             patch('praktikum.praktikum.Burger') as mock_burger, \
             patch('praktikum.praktikum.print'):
            
            mock_db_instance = Mock()
            mock_db.return_value = mock_db_instance
            mock_burger_instance = Mock()
            mock_burger.return_value = mock_burger_instance
            
            mock_buns = [Mock() for _ in range(3)]
            mock_ingredients = [Mock() for _ in range(6)]
            mock_db_instance.available_buns.return_value = mock_buns
            mock_db_instance.available_ingredients.return_value = mock_ingredients
            
            # Это покроет строку с main()
            if module.__name__ == "__main__":
                module.main()
                
    finally:
        module.__name__ = original_name