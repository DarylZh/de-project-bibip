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
        self.update_index(self.cars_index_file, str(car.vin), self.get_line_count(self.cars_file) - 1) 
        return car 

    def add_model(self, model: Model) -> Model: 
        # Запись модели в models.txt 
        with open(self.models_file, 'a') as f: 
            line = f"{model.id};{model.name};{model.brand}\n" 
            f.write(line) 
        # Обновление индекса 
        self.update_index(self.models_index_file, str(model.id), self.get_line_count(self.models_file) - 1) 
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
        # Получение количества строк в файле 
        with open(file_path, 'r') as f: 
            return sum(1 for _ in f) 

    def get_line_number_by_vin(self, vin: str) -> int | None:
        # Получение номера строки автомобиля по VIN
        if os.path.exists(self.cars_index_file):
            with open(self.cars_index_file, 'r') as f:
                for line in f:
                    key, line_num = line.strip().split(';')
                    if key == vin:
                        return int(line_num)
        return None  # Если VIN не найден

    # Задание 2. Сохранение продаж  
    def sell_car(self, sale: Sale) -> Car:  
        # 1. Запись продажи в sales.txt  
        with open(self.sales_file, 'a') as f:  
            line = f"{sale.sales_number};{sale.car_vin};{sale.cost};{sale.sales_date}\n"  
            f.write(line)  

        # 2. Обновление индекса продаж  
        self.update_index(self.sales_index_file, str(sale.sales_number), self.get_line_count(self.sales_file) - 1)  

        # 3. Найти автомобиль в cars.txt  
        car_line_number = self.get_line_number_by_vin(sale.car_vin)  
        if car_line_number is not None:
            raise ValueError(f"Car with VIN {sale.car_vin} not found")
        # 4a. Чтение автомобиля из cars.txt  
        with open(self.cars_file, 'r') as f:
            lines = f.readlines()  
            car_line = lines[car_line_number].strip().split(';') 

        # 4b. Обновление статуса автомобиля 
            car_line[4] = 'sold' 

        # 4c. Запись обновленного автомобиля обратно в cars.txt
            lines[car_line_number] = ';'.join(car_line) + '\n'
            with open(self.cars_file, 'w') as f:
                f.writelines(lines)

    # Возвращаем объект автомобиля
            return self.parse_car(car_line)
        
    # Задание 3. Доступные к продаже
class CarStatus:
    AVAILABLE = "available"
    SOLD = "sold"
    # другие статусы...

class Car:
    def __init__(self, vin, model, price, date_start, status):
        self.vin = vin
        self.model = model
        self.price = price
        self.date_start = date_start
        self.status = status

    def __repr__(self):
        return f"Car(vin={self.vin}, model={self.model}, status={self.status})"

    def get_cars(self, status: CarStatus) -> list[Car]:
        available_cars = []
        if not os.path.exists(self.cars_file):
            return available_cars
            
        with open(self.cars_file, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) >= 5 and parts[4] == status.value:
                    available_cars.append(self.parse_car(parts))
        return available_cars

    # Задание 4. Вывод детальной информации
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # Находим автомобиль
        car_line_number = self.get_line_number_by_vin(vin)
        if car_line_number is None:
            return None

        with open(self.cars_file, 'r') as f:
            lines = f.readlines()
            car_line = lines[car_line_number].strip().split(';')
            car = self.parse_car(car_line)

        # Находим модель автомобиля
        model_id = car.model
        model = None
        if os.path.exists(self.models_index_file):
            with open(self.models_index_file, 'r') as f:
                for line in f:
                    parts = line.strip().split(';')
                    if parts[0] == str(model_id):
                        model_line_number = int(parts[1])
                        with open(self.models_file, 'r') as mf:
                            model_lines = mf.readlines()
                            model_data = model_lines[model_line_number].strip().split(';')
                            model = Model(
                                id=int(model_data[0]),
                                name=model_data[1],
                                brand=model_data[2]
                            )
                        break

        # Находим продажи для этого автомобиля
        sales = []
        if os.path.exists(self.sales_file):
            with open(self.sales_file, 'r') as f:
                for line in f:
                    parts = line.strip().split(';')
                    if parts[1] == vin:
                        sales.append(Sale(
                            sales_number=int(parts[0]),
                            car_vin=parts[1],
                            cost=Decimal(parts[2]),
                            sales_date=parts[3]
                        ))

        return CarFullInfo(
            car=car,
            model=model,
            sales=sales
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
    car_data = lines[car_index].strip().split(';')
    car_data[0] = new_vin  # Обновляем VIN-код
    lines[car_index] = ';'.join(car_data) + '\n'  # Обновляем строку

    # Записываем обновленный список автомобилей в cars.txt
    with open(self.cars_file, 'w') as cars_file:
        cars_file.writelines(lines)

    # Обновляем индекс
    index_data[car_index][0] = new_vin  # Обновляем VIN в индексе

    # Сортируем индекс
    index_data.sort(key=lambda x: x[0])  # Сортировка по VIN

    # Записываем обновленный индекс обратно в файл
    with open(self.cars_index_file, 'w') as index_file:
        for entry in index_data:
            index_file.write(';'.join(entry) + '\n')

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
        
