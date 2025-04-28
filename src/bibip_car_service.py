from decimal import Decimal
from typing import List, Optional
from models import Car, Model, Sale, CarFullInfo, CarStatus

class CarService:
    def __init__(self, rood_dir) -> None:
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

    def update_vin(self, old_vin: str, new_vin: str) -> None:
        car = next((car for car in self.cars if car.vin == old_vin), None)
        if car is None:
            raise ValueError(f"Car with VIN {old_vin} not found")
        
        # Обновление VIN номера
        car.vin = new_vin

        # Обновление всех продаж, связанных с этим автомобилем
        for sale in self.sales:
            if sale.car_vin == old_vin:
                sale.car_vin = new_vin

    def revert_sale(self, sale_id: int) -> None:
        sale = next((sale for sale in self.sales if sale.id == sale_id), None)
        if sale is None:
            raise ValueError(f"Sale with ID {sale_id} not found")

        # Удаление продажи из списка
        self.sales.remove(sale)

        # Обновление статуса автомобиля на "Доступен"
        car = next((car for car in self.cars if car.vin == sale.car_vin), None)
        if car:
            car.status = CarStatus.AVAILABLE  # Предполагаем, что статус "Доступен"
            
    def top_models_by_sales(self) -> List[ModelSaleStats]:
    sales_count = {}
    
        # Чтение данных о продажах
        for sale in self.sales:
            model_id = sale.car_vin  # Предполагается, что VIN соответствует модели
            sales_count[model_id] = sales_count.get(model_id, 0) + 1

        # Получение списка моделей с количеством продаж
        sorted_sales = sorted(sales_count.items(), key=lambda item: (-item[1], self.get_model_price(item[0])))

        # Берем топ-3 модели
        top_models = []
        for model_id, count in sorted_sales[:3]:
            model = self.get_model_by_id(model_id)  # Метод для получения модели по ID
            if model:
                
    top_models.append(ModelSaleStats(car_model_name=model.name, brand=model.brand, sales_number=count))

        return top_models

    def get_model_price(self, model_id: str) -> Decimal:
        # Метод для получения цены модели по ID
        model = next((m for m in self.models if m.id == model_id), None)
        return model.price if model else Decimal(0)

    def get_model_by_id(self, model_id: str) -> Optional[Model]:
        # Метод для получения модели по ID
        return next((m for m in self.models if m.id == model_id), None)
