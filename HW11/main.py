from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self.value = value
        

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        if len(new_value) == 10 and new_value.isdigit():
            self.__value = new_value
        else:
            raise ValueError("invalid phone number")

    def __str__(self):
        return self.value
    

class InvalidBirthdayError(Exception):
    pass


class Birthday(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, date_birthday: str):
        try:
            date_time_obj = datetime.strptime(date_birthday, '%d-%m-%Y')
            self.__value = date_time_obj
        except ValueError:
            raise InvalidBirthdayError("Invalid birthday format")




class Record:
    def __init__(self, name_):
        self.name = Name(name_)
        print(self.name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            birthday = self.birthday.value
            current_day = datetime.now()
            birthday = birthday.replace(year=current_day.year)
            if birthday == current_day:
                days = 0
            elif birthday < current_day:
                days = (birthday.replace(year=current_day.year+1) - current_day).days
            else:
                days = (birthday.replace(year=current_day.year) - current_day).days
            return days


    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def remove_phone(self, phone_number):
        phone_object = self.find_phone(phone_number)
        if phone_object:
            self.phones.remove(phone_object)

    def edit_phone(self, phone_old_number, phone_new_number):
        phone_object = self.find_phone(phone_old_number)
        if phone_object:
            phone_object.value = phone_new_number
        else:
            raise ValueError

    def __str__(self):
        return (f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, "
                f"birthday: {self.birthday.value if self.birthday else 'no' }")


class AddressBook(UserDict):

    def iterator(self, n: int = 2):
        result = f"{'-'*50}\n"
        count = 0
        id_ = 0
        for name, record in self.data.items():
            result += f"{id_}: {record}\n"
            id_ += 1
            count += 1
            if count >= n:
                yield result
                count = 0
                result = f"{'-'*50}\n"
        yield result

    def add_record(self, record_: Record):
        self.data[record_.name.value] = record_

    def find(self, name_):
        return self.data.get(name_)

    def delete(self, name_):
        record_book = self.find(name_)
        if record_book:
            del self.data[name_]


    def save_to_file(self, file_path='address_book.pkl'):
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)


    def load_from_file(self, file_path='address_book.pkl'):
        try:
            with open(file_path, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new address book.")


    def search(self, query):
        results = {}
        for name, record in self.data.items():
            if query.lower() in name.lower():
                results[name] = record
            else:
                for phone in record.phones:
                    if query in phone.value:
                        results[name] = record
                        break
        return results



if __name__ == "__main__":
    book = AddressBook()

    book.save_to_file()
    book.load_from_file()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("29-04-1992")

    john1_record = Record("John1")
    john1_record.add_phone("1234567890")
    john1_record.add_phone("5555555555")
    john1_record.add_birthday("29-11-1990")


    john2_record = Record("John2")
    john2_record.add_phone("1234567890")
    john2_record.add_phone("7777777777")
    john2_record.add_birthday("10-12-1995")


    try:
        john_record.add_birthday("invalid_date_format")  # Викинет виняток InvalidBirthdayError
    except InvalidBirthdayError as e:
        print(f"Caught an error outside Birthday class: {e}")


    # Додавання запису John до адресної книги
    book.add_record(john_record)
    book.add_record(john1_record)
    book.add_record(john2_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)


    search_query = input('Enter name or phone number to search: ')
    search_results = book.search(search_query)

    if search_results:
        print('\nSearch results:')
        for name, record in search_results.items():
            print(record)
    else:
        print('No matching records found.')

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    print(john)
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555


    # Видалення запису Jane
    book.delete("Jane")
    gen = book.iterator(2)
    r = next(gen)
    print(r)