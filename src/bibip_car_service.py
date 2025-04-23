import os
from datetime import datetime
from decimal import Decimal
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        self.cars_file = os.path.join(root_directory_path, 'cars.txt')
        self.cars_index_file = os.path.join(root_directory_path, 'cars_index.txt')
        self.models_file = os.path.join(root_directory_path, 'models.txt')
        self.models_index_file = os.path.join(root_directory_path, 'models_index.txt')
        self.sales_file = os.path.join(root_directory_path, 'sales.txt')
        self.sales_index_file = os.path.join(root_directory_path, 'sales_index.txt')

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        # Запись автомобиля в cars.txt
        with open(self.cars_file, 'a') as f:
            line = f"{car.vin};{car.model};{car.price};{car.date_start};{car.status}\n"
            f.write(line)

        # Обновление индекса
        self.update_index(self.cars_index_file, car.vin, self.get_line_count(self.cars_file) - 1)
        return car

    def add_model(self, model: Model) -> Model:
        # Запись модели в models.txt
        with open(self.models_file, 'a') as f:
            line = f"{model.id};{model.name};{model.brand}\n"
            f.write(line)

        # Обновление индекса
        self.update_index(self.models_index_file, model.id, self.get_line_count(self.models_file) - 1)
        return model

    def update_index(self, index_file: str, key: str, line_number: int) -> None:
        # Чтение существующего индекса
        index_data = []
        if os.path.exists(index_file):
            with open(index_file, 'r') as f:
                index_data = [line.strip().split(';') for line in f]

        # Добавление новой записи
        index_data.append((key, line_number))

        # Сортировка индекса
        index_data.sort(key=lambda x: x[0])

        # Запись обновленного индекса обратно в файл
        with open(index_file, 'w') as f:
            for key, line_num in index_data:
                f.write(f"{key};{line_num}\n")

    def get_line_count(self, file_path: str) -> int:
        # Подсчет количества строк в файле
        if not os.path.exists(file_path):
            return 0
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)

    # Задание 2. Сохранение продаж
    def sell_car(self, sale: Sale) -> Car:
        # 1. Запись продажи в sales.txt
        with open(self.sales_file, 'a') as f:
            line = f"{sale.sales_number};{sale.car_vin};{sale.cost};{sale.sales_date}\n"
            f.write(line)

        # 2. Обновление индекса продаж
        self.update_index(self.sales_index_file, sale.sales_number, self.get_line_count(self.sales_file) - 1)

        # 3. Найти автомобиль в cars.txt
        car_line_number = self.get_line_number_by_vin(sale.car_vin)
        if car_line_number is not None:
            # 4a. Чтение автомобиля из cars.txt
            with open(self.cars_file, 'r') as f:
                lines = f.readlines()
                car_line = lines[car_line_number].strip().split(';')

            # 4b. Обновление статуса автомобиля
            car_line[4] = 'sold'  # Обновляем статус на sold

            # 4c. Запись обновленного автомобиля обратно в cars.txt
            with open(self.cars_file, 'r+') as f:
                f.seek(car_line_number * 501)  # Позиция строки (длина строки 500 + 1 символ на \n)
                f.write(';'.join(car_line).ljust(500) + '\n')  # Записываем обновленную строку

        return sale

    def get_line_number_by_vin(self, vin: str) -> int | None:
        with open(self.cars_index_file, 'r') as f:
            for line in f:
                index_vin, line_number = line.strip().split(';')
                if index_vin == vin:
                    return int(line_number)
        return None

    def get_line_count(self, file_path: str) -> int:
        # Подсчет количества строк в файле
        if not os.path.exists(file_path):
            return 0
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)
 
# Пример использования
if __name__ == "__main__":
    service = CarService('path_to_directory')

    # Пример продажи автомобиля
    sale = Sale('123#4321', '1HGBH41JXMN109186', 99999.99, '2024-10-01')
    service.sell_car(sale)
  
    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        raise NotImplementedError
 
class CarStatus:
    AVAILABLE = "available"
    SOLD = "sold"
    # другие статусы...

class Car:
    def __init__(self, vin, model, status):
        self.vin = vin
        self.model = model
        self.status = status

    def __repr__(self):
        return f"Car(vin={self.vin}, model={self.model}, status={self.status})"

class CarDealership:
    def __init__(self, cars):
        self.cars = cars  # список автомобилей

    def get_cars(self, status: CarStatus) -> list[Car]:
        available_cars = [car for car in self.cars if car.status == status.AVAILABLE]
        return sorted(available_cars, key=lambda car: car.vin)

# Пример использования
if __name__ == "__main__":
    cars = [
        Car("1HGCM82633A123456", "Honda Accord", CarStatus.AVAILABLE),
        Car("1HGCM82633A654321", "Honda Civic", CarStatus.SOLD),
        Car("1HGCM82633A987654", "Toyota Camry", CarStatus.AVAILABLE),
    ]

    dealership = CarDealership(cars)
    available_cars = dealership.get_cars(CarStatus)
    print(available_cars) 
 
    # Задание 3. Вывод машин, доступных к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        available_cars = []
        with open(self.cars_file, 'r') as f:
            for line in f:
                vin, model, price, date_start, car_status = line.strip().split(';')
                if car_status == status.AVAILABLE:
                    available_cars.append(Car(vin, int(model), price, date_start, car_status))
        return sorted(available_cars, key=lambda car: car.vin)

    # Задание 4. Вывод детальной информации
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # Читаем данные об автомобиле
        with open(self.cars_index_file, 'r') as index_file:
            for line in index_file:
                index_data = line.strip().split(';')
                if index_data[0] == vin:
                    car_line_number = int(index_data[1])  # Номер строки в cars.txt
                    break
            else:
                return None  # Если VIN не найден

        # Читаем данные из cars.txt
        with open(self.cars_file, 'r') as cars_file:
            car_data = cars_file.readlines()[car_line_number].strip().split(';')

        # Читаем данные о модели
        model_id = car_data[1]
        with open(self.models_index_file, 'r') as model_index_file:
            for line in model_index_file:
                model_index_data = line.strip().split(';')
                if model_index_data[0] == model_id:
                    model_line_number = int(model_index_data[1])
                    break

        # Читаем данные из models.txt
        with open(self.models_file, 'r') as models_file:
            model_data = models_file.readlines()[model_line_number].strip().split(';')

        # Проверяем статус автомобиля
        car_status = car_data[4]
        sales_date = None
        sales_cost = None

        if car_status == 'sold':
            # Читаем данные о продаже
            with open(self.sales_file, 'r') as sales_file:
                for line in sales_file:
                    sales_data = line.strip().split(';')
                    if sales_data[1] == vin:
                        sales_date = sales_data[2]  # Дата продажи
                        sales_cost = sales_data[3]  # Цена продажи
                        break

        # Возвращаем объект CarFullInfo
        return CarFullInfo(
            vin=vin,
            model_name=model_data[1],  # Имя модели
            model_brand=model_data[2],  # Бренд модели
            price=float(car_data[2]),  # Закупочная стоимость
            date_start=car_data[3],  # Дата поступления
            status=car_status,
            sales_date=sales_date,
            sales_cost=sales_cost
        )

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> None:
        # Читаем индекс
        with open(self.cars_index_file, 'r') as index_file:
            index_data = [line.strip().split(';') for line in index_file]
        
        # Находим строку с автомобилем
        car_index = None
        for i, (key, _) in enumerate(index_data):
            if key == vin:
                car_index = i
                break
        
        if car_index is None:
            print("Автомобиль с указанным VIN не найден.")
            return
        
        # Читаем данные об автомобиле
        with open(self.cars_file, 'r') as cars_file:
            lines = cars_file.readlines()
        
        # Обновляем VIN-код
        cars[car_index].vin = new_vin

        # Записываем обновленный автомобиль в cars.txt
        write_cars('cars.txt', cars)

        # Обновляем индекс
        index[car_index] = car_index  # индекс остается тем же, но можно добавить логику для сортировки
        index.sort()  # если нужно отсортировать

        # Записываем обновленный индекс в car_index.txt
        write_index('car_index.txt', index)
    else:
        print("Автомобиль с указанным VIN не найден.")

# Пример использования
update_vin('OLD_VIN123', 'NEW_VIN456')
  
    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> None:
        # Читаем данные о машинах и продажах
        cars = self.read_cars(self.cars_file)
        sales = self.read_sales(self.sales_file)

        # Удаляем запись о продаже
        updated_sales = []
        sale_found = False
        vin = None

        for sale in sales:
            if sale[0] == sales_number:
                sale_found = True  # Запись о продаже найдена
                vin = sale[1]  # Получаем VIN автомобиля
            else:
                updated_sales.append(sale)

        # Если запись о продаже найдена, обновляем статус машины
        if sale_found and vin:
            for car in cars:
                if car.vin == vin:
                    car.mark_as_unsold()  # Обновляем статус машины
                    break

            # Записываем обновленные данные обратно в файлы
            self.write_cars(self.cars_file, cars)
            self.write_sales(self.sales_file, updated_sales)
            print(f"Запись о продаже {sales_number} удалена, статус машины {vin} обновлен.")
        else:
            print(f"Запись о продаже {sales_number} не найдена.")

    def read_cars(self, file_path):
        cars = []
        with open(file_path, 'r') as f:
            for line in f:
                vin, model, year, is_sold = line.strip().split(',')
                cars.append(Car(vin, model, year, is_sold == 'True'))
        return cars

    def write_cars(self, file_path, cars):
        with open(file_path, 'w') as f:
            for car in cars:
                f.write(f"{car.vin},{car.model},{car.year},{car.is_sold}\n")

    def read_sales(self, file_path):
        sales = []
        with open(file_path, 'r') as f:
            for line in f:
                sales_number, vin, sale_date = line.strip().split(',')
                sales.append((sales_number, vin, sale_date))
        return sales

    def write_sales(self, file_path, sales):
        with open(file_path, 'w') as f:
            for sale in sales:
                f.write(f"{sale[0]},{sale[1]},{sale[2]}\n")
 
    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        sales_count = {}
        sales = self.read_sales(self.sales_file)

        for sale in sales:
            model_id = sale[1]  # берем id модели
            sales_count[model_id] = sales_count.get(model_id, 0) + 1

        # Сортируем словарь по количеству продаж и цене
        sorted_sales = sorted(sales_count.items(), key=lambda item: (-item[1], -self.get_model_price(item[0])))

        # Берем первые 3 модели
        top_models= sorted_sales[:3]

        # Формируем объекты ModelSaleStats
        model_stats = []
        for model_id, count in top_models:
            model_info = self.get_model_info(model_id)
            model_stats.append(ModelSaleStats(model_info[1], model_info[2], count))

        return model_stats

    def get_model_price(self, model_id):
        models = self.read_models(self.models_file)
        for model in models:
            if model[0] == model_id:
                return model[3]  # Возвращаем цену модели
        return 0

    def get_model_info(self, model_id):
        models = self.read_models(self.models_file)
        for model in models:
            if model[0] == model_id:
                return model  # Возвращаем информацию о модели
        return None

    def read_models(self, file_path):
        models
        
# Пример использования
top_models = top_models_by_sales()
for model in top_models:
    print(f"Модель: {model.car_model_name}, Бренд: {model.brand}, Количество продаж: {model.sales_count}")
 
