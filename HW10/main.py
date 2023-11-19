from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

        if self.is_valid_phone(value):
            self.value = value
        else:
            raise ValueError

    @staticmethod
    def is_valid_phone(value: str):
        if len(value) == 10 and value.isdigit():
            return True
        else:
            return False

    def __str__(self):
        return self.value


class Record:
    def __init__(self, name_):
        self.name = Name(name_)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone_number):
       

            for phone in self.phones:
                if phone.value == phone_number:
                    return phone
            raise ValueError
        

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
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record_: Record):
        self.data[record_.name.value] = record_

    def find(self, name_):
        return self.data.get(name_)

    def delete(self, name_):
        record_book = self.find(name_)
        if record_book:
            del self.data[name_]


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

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