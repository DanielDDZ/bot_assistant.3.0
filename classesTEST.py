from collections import UserDict
import re


class Field:
    def __init__(self):
        self._value = ''

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self):
        for key, record in self.data.items():
            yield key, record


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, phone):
        if re.match(r'^0\d{9}$', phone):
            self._value = phone
            return True


class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.add_phone(new_phone)
                self.phones.remove(phone)
                return True

    def delete_phone(self, new_phone):
        for phone in self.phones:
            if phone.value == new_phone:
                self.phones.remove(phone)
                return True
