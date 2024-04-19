import pickle
from datetime import datetime, timedelta

class InputError(Exception):
    pass
           
class Birthday:
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")   

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None
        
    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            raise ValueError("Birthday must be an instance of the Birthday class")
        self.birthday = birthday
    
    def add_phone(self, phone_number):
        self.phones.append(phone_number)
           
    def show_birthday(self):
        if self.birthday:
            return f"{self.name} birthday: {self.birthday.value.strftime("%d.%m.%Y")}"
        else:
            return f"{self.name} does not have a recorded birthday."            

class AddressBook:
    def __init__(self):
        self.contacts = {}
    
    def show_phone(self, name):
        record = self.find(name)
        if record:
            return f"{name} phone numbers: {', '.join(record.phones)}"
        else:
            return f"{name} not found in the address book." 

    def find(self, name):
        return self.contacts.get(name)

    def add_record(self, record):
        if record.name in self.contacts:
            existing_record = self.contacts[record.name]
            existing_record.phones.extend(record.phones)
            if record.birthday:
                existing_record.add_birthday(record.birthday)
        else:
             self.contacts[record.name] = record      
        
def parse_input(user_input):
    parts = user_input.split(maxsplit = 1)
    cmd = parts[0].strip().lower()
    args = parts[1].strip().split() if len(parts) > 1 else []
    return cmd, *args

def add_contact(args, book: AddressBook):
        if len(args) < 2:
            raise InputError("Give me name and phone please.")
        name, *phones = args
        for phone in phones:
            if len(phone) != 10 or not phone.isdigit():
                raise InputError("Phone number should contain exactly 10 digits.")
        record = book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = "Contact added."
        record.phones.extend(phones)
        return message        

def change_contact(args, book: AddressBook):
    if len(args) < 2:
        raise InputError("Give me name and new phone please.")
    name, *phones = args
    for phone in phones:
        if len(phone) != 10 or not phone.isdigit():
            raise InputError("Phone number should contain exactly 10 digits.")
    if name in book.contacts:
        book.contacts[name].phones = phones
        return f"Phone number updated for {name}."
    else:
        return f"{name} not found in the address book."            

def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise InputError("Give me name and birthday please.")
    name, birthday = args
    if name in book.contacts:
        book.contacts[name].add_birthday(Birthday(birthday))
        return f"Birthday added for {name}."
    else:        
        return f"{name} not found in the address book."
    
def show_birthday(name, book: AddressBook):
        record = book.find(name)
        if record:
            return record.show_birthday()
        else:
            return f"{name} not found in the address book."       
    
def birthdays(book: AddressBook):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    upcoming_birthdays = []
    for name, record in book.contacts.items():
        if record.birthday:
            birthday_this_year = record.birthday.value.replace(year = today.year).date()
            if birthday_this_year >= today:
                if birthday_this_year < next_week:
                    upcoming_birthdays.append(record.show_birthday())
            else:
                next_birthday = birthday_this_year.replace(year = today.year + 1)
                if next_birthday < next_week:
                    upcoming_birthdays.append(record.show_birthday())        
    return "Upcoming birthdays:\n" + "\n".join(upcoming_birthdays)

def show_all(book: AddressBook):
    all_contacts = book.contacts.values()
    contacts_info = []
    for record in all_contacts:
        phones = record.phones
        contacts_info.append(f"{record.name} Phones: {', '.join(phones)}")
    return "\n".join(contacts_info)    

def save_data(book: AddressBook, filename = "addressbook.pk1"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename = "addressbook.pk1"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            try:
                print(add_contact(args, book))
            except InputError as e:
                print(e)     

        elif command == "change":
            try:
                print(change_contact(args, book))
            except InputError as e:
                print(e)    

        elif command == "phone":
            print(book.show_phone(*args))  

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            try:
                print(add_birthday(args, book))
            except InputError as e:
                print(e)    

        elif command == "show-birthday":
            print(show_birthday(*args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()


      