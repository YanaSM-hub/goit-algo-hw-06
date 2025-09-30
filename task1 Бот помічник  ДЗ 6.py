from collections import UserDict


# ====== Класи для контактів ======

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        self.phones = [p for p in self.phones if p.value != phone.value]

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone.value:
                self.phones[i] = new_phone
                return
        raise ValueError("Phone not found.")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = ", ".join(p.value for p in self.phones)
        return f"{self.name.value}: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]


# ====== Декоратор для обробки помилок ======

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e) if str(e) else "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command."
    return wrapper


# ====== CLI-функції ======

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(Phone(phone))
    else:
        record = Record(Name(name))
        record.add_phone(Phone(phone))
        book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    record = book.find(name)
    if record:
        record.phones = [Phone(phone)]
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(args, book: AddressBook):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    return ", ".join(p.value for p in record.phones)


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


# ====== Основна функція ======

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
        except ValueError:
            print("Invalid command.")
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

    
    

    