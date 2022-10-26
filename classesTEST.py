from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, count=0):
        records = []
        count = count if count else len(self.data)
        for record in self.data.values():
            if len(records) >= count:
                yield records
                records = []
            records.append(record)
        if records:
            yield records


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value: str):
        super().__init__(value)
        self.value = value

    @Field.value.setter
    def value(self, phone):
        if re.search(r'^0\d{9}$', phone):
            self._value = phone
        else:
            raise ValueError(f"Phone number {phone} is not valid")
        return phone


class Birthday(Field):

    @Field.value.setter
    def value(self, birthday):
        if int(birthday.year) <= 2022 and int(birthday.month) <= 12 and int(birthday.day) <= 31:
            self._value = datetime(year=datetime.now().year, month=int(birthday.month),
                                   day=int(birthday.day))
        else:
            print('Birthday entered incorrectly')


class Record(Field):
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday()
        if birthday:
            self.birthday.value = birthday

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

    def days_to_birthday(self):
        if not self.birthday:
            return 'You did not enter a birthday'
        now = datetime.now()
        if int(self.birthday.value.month) <= int(now.month) and int(self.birthday.value.day) != int(now.day):
            days_to_birthday = self.birthday.value - \
                now.replace(year=(int(now.year) - 1)) + timedelta(days=1)
            return days_to_birthday.days
        days_to_birthday = self.birthday.value - now + timedelta(days=1)
        return days_to_birthday.days
