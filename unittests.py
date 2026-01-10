import unittest
from models import Expense, Car

class TestCar(unittest.TestCase):
    def setUp(self):
        self.car = Car(
            id=0,
            model='Kia Rio',
            year='2016',
            mileage=35000,
            price=1200000,
        )

        expense = Expense(
            id=0,
            car_id=self.car.id,
            amount=1000,
            category='Другое',
            date='2025-12-01',
            description='тест',
            mileage=36000
        )

        self.car.expenses.append(expense)

    def test_mileage(self):
        """
        Тестирует корректное создание объекта
        """
        self.assertEqual(self.car.mileage, 35000.0)

    def test_independency(self):
        """
        Тестирует инкапсуляцию
        """
        second_car = Car(
            id=1,
            model='Hyundai Solaris',
            year='2017',
            mileage=45000,
            price=1100000,
        )
        self.assertNotEqual(self.car.year, second_car.year)

    def test_expenses(self):
        """
        Тестирует подсчет расхода руб/км
        """
        exp = self.car.calculate_expense()
        self.assertEqual(exp, 1.0)

    def test_validate_year(self):
        """
        Тестирует работу статического метода валидации года выпуска А/М
        """
        with self.assertRaises(ValueError): #
            Car(
                id=2,
                model='Hyundai Solaris',
                year='1775',
                mileage=45000,
                price=1100000,
            )


if __name__ == '__main__':
    unittest.main(argv=[''])
