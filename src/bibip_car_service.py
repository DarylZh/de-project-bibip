from decimal import Decimal
from typing import List, Optional

class CarStatus:
    AVAILABLE = "available"
    SOLD = "sold"

class Model:
    def __init__(self, id: int, name: str, brand: str):
        self.id = id
        self.name = name
        self.brand = brand

class Car:
    def __init__(self, vin: str, model_id: int, price: Decimal, date_start: str, status: str = CarStatus.AVAILABLE):
        self.vin = vin
        self.model_id = model_id
        self.price = price
        self.date_start = date_start
        self.status = status

class Sale:
    def __init__(self, sales_number: int, car_vin: str, cost: Decimal, sales_date: str):
        self.sales_number = sales_number
        self.car_vin = car_vin
        self.cost = cost
        self.sales_date = sales_date

class CarFullInfo:
    def __init__(self, vin: str, car_model_name: str, car_model_brand: str, price: Decimal, date_start: str, status: str, sales_date: Optional[str], sales_cost: Optional[Decimal]):
        self.vin = vin
        self.car_model_name = car_model_name
        self.car_model_brand = car_model_brand
        self.price = price
        self.date_start = date_start
        self.status = status
        self.sales_date = sales_date
        self.sales_cost = sales_cost

class CarService:
    def __init__(self) -> None:
        self.models: List[Model] = []  # Список для хранения моделей
        self.cars: List[Car] = []       # Список для хранения автомобилей
        self.sales: List[Sale] = []      # Список для хранения продаж

    def add_car(self, car: Car) -> Car:
        self.cars.append(car)
        return car

    def add_model(self, model: Model) -> Model:
        self.models.append(model)
        return model

    def sell_car(self, sale: Sale) -> Car:
        # Проверка наличия автомобиля
        car = next((car for car in self.cars if car.vin == sale.car_vin), None)
        if car is None:
            raise ValueError(f"Car with VIN {sale.car_vin} not found")

        # Запись продажи
        self.sales.append(sale)

        # Обновление статуса автомобиля
        car.status = CarStatus.SOLD

        return car

    def get_car_info(self, vin: str) -> Optional[CarFullInfo]:
        car = next((car for car in self.cars if car.vin == vin), None)
        if not car:
            return None

        model = next((model for model in self.models if model.id == car.model_id), None)
        sales_for_car = [sale for sale in self.sales if sale.car_vin == vin]

        sales_date = sales_for_car[0].sales_date if sales_for_car else None
        sales_cost = sales_for_car[0].cost if sales_for_car else None

        return CarFullInfo(
            vin=car.vin,
            car_model_name=model.name if model else "Unknown",
            car_model_brand=model.brand if model else "Unknown",
            price=car.price,
            date_start=car.date_start,
            status=car.status,
            sales_date=sales_date,
            sales_cost=sales_cost,
        )

    def get_cars_by_status(self, status: str) -> List[Car]:
        return [car for car in self.cars if car.status == status]

    def top_models_by_sales(self) -> List[tuple[str, int]]:
        sales_count = {}
        for sale in self.sales:
            model_id = sale.car_vin  # Предполагаем, что VIN соответствует модели
            sales_count[model_id] = sales_count.get(model_id, 0) + 1

        # Сортировка по количеству продаж
        sorted_sales = sorted(sales_count.items(), key=lambda item: item[1], reverse=True)

        # Берем топ-3 модели
        return sorted_sales[:3]

