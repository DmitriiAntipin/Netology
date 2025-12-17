class Customer:
    def __init__(self, name, device_type, browser, sex, age, bill, region):
        self.name = name
        self.device_type = device_type
        self.browser = browser
        self.sex = sex
        self.age = age
        self.bill = bill
        self.region = region
    def get_russian_gender(self):
        if self.sex.lower() == 'female':
            return 'женского'
        elif self.sex.lower() == 'male':
            return 'мужского'
        else:
            return 'неизвестного'
    def get_russian_verb(self):
        if self.sex.lower() == 'female':
            return 'совершила'
        elif self.sex.lower() == 'male':
            return 'совершил'
        else:
            return 'совершил(а)'
    def get_device_description(self):
        device_map = {
            'mobile': 'мобильного',
            'desktop': 'десктопного',
            'laptop': 'ноутбука',
            'tablet': 'планшета'
        }
        return device_map.get(self.device_type.lower(), self.device_type)
    def generate_description(self):
        gender = self.get_russian_gender()
        verb = self.get_russian_verb()
        device_desc = self.get_device_description()
        description = (f"Пользователь {self.name} {gender} пола, "
                       f"{self.age} лет {verb} покупку на {self.bill} у.е. "
                       f"с {device_desc} браузера {self.browser}. ")
        if self.region and self.region != '-':
            description += f"Регион, из которого совершалась покупка: {self.region}."
        else:
            description += "Регион покупки не указан."
        return description

class CSVReader:
    @staticmethod
    def read_csv(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"Ошибка: Файл {filename} не найден.")
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

    @staticmethod
    def parse_csv_data(lines):
        if not lines:
            return []
        headers = lines[0].strip().split(',')
        data = []
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            values = []
            i = 0
            in_quotes = False
            current_value = []
            while i < len(line):
                if line[i] == '"':
                    in_quotes = not in_quotes
                    i += 1
                elif line[i] == ',' and not in_quotes:
                    values.append(''.join(current_value))
                    current_value = []
                    i += 1
                else:
                    current_value.append(line[i])
                    i += 1
            values.append(''.join(current_value))
            if len(values) == len(headers):
                data.append(dict(zip(headers, values)))

        return data


class CustomerDescriptionGenerator:
    @staticmethod
    def create_customers_from_data(data):
        customers = []
        for item in data:
            try:
                customer = Customer(
                    name=item.get('name', ''),
                    device_type=item.get('device_type', ''),
                    browser=item.get('browser', ''),
                    sex=item.get('sex', ''),
                    age=int(item.get('age', 0)) if item.get('age', '').isdigit() else 0,
                    bill=int(item.get('bill', 0)) if item.get('bill', '').isdigit() else 0,
                    region=item.get('region', '')
                )
                customers.append(customer)
            except Exception as e:
                print(f"Ошибка при создании покупателя: {e}")
                continue
        return customers
    @staticmethod
    def generate_descriptions(customers):
        descriptions = []
        for customer in customers:
            try:
                description = customer.generate_description()
                descriptions.append(description)
            except Exception as e:
                print(f"Ошибка при генерации описания: {e}")
                continue
        return descriptions

class FileWriter:
    @staticmethod
    def write_to_txt(filename, descriptions):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for i, description in enumerate(descriptions, 1):
                    file.write(f"{i}. {description}\n\n")
            print(f"Успешно записано {len(descriptions)} описаний в файл {filename}")
            return True
        except Exception as e:
            print(f"Ошибка при записи в файл: {e}")
            return False

def main():
    input_filename = 'web_clients_correct.csv'
    output_filename = 'customers_descriptions.txt'
    csv_reader = CSVReader()
    lines = csv_reader.read_csv(input_filename)
    if not lines:
        print("Не удалось загрузить данные.")
        return
    data = csv_reader.parse_csv_data(lines)
    generator = CustomerDescriptionGenerator()
    customers = generator.create_customers_from_data(data)
    descriptions = generator.generate_descriptions(customers)
    writer = FileWriter()
    if writer.write_to_txt(output_filename, descriptions):
        print(f"\nПрограмма успешно завершена!")
    else:
        print("Не удалось записать результаты в файл.")

if __name__ == "__main__":
    main()