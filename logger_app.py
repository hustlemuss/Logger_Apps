import csv
import re
from datetime import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"{datetime.now()} ")
                log_file.write(f"Function: {old_function.__name__} ")
                log_file.write(f"Args: {args}, Kwargs: {kwargs}\n")
            result = old_function(*args, **kwargs)
            return result
        return new_function
    return __logger

@logger("scraping_log.txt")
def format_phone(phone):
    phone_pattern = r'(\+?\d{1,2})?[\s\(\)-]*(\d{3})[\s\(\)-]*(\d{3})[\s\(\)-]*(\d{2})[\s\(\)-]*(\d{2})[\s\(\)-]*доб\.\s*(\d+)?'
    match = re.match(phone_pattern, phone)
    if match:
        groups = match.groups()
        formatted_phone = f"+7({groups[1]}){groups[2]}-{groups[3]}-{groups[4]}"
        if groups[5]:
            formatted_phone += f" доб.{groups[5]}"
        return formatted_phone
    else:
        return None

@logger("scraping_log.txt")
def process_contacts(contacts):
    processed_contacts = {}
    for contact in contacts:
        lastname, firstname, surname = contact[0], contact[1], contact[2]
        key = (lastname, firstname, surname)
        if key in processed_contacts:
            existing_contact = processed_contacts[key]
            for i in range(len(contact)):
                if not existing_contact[i]:
                    existing_contact[i] = contact[i]
            processed_contacts[key] = existing_contact
        else:
            processed_contacts[key] = contact
    return list(processed_contacts.values())

def main():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    processed_contacts = process_contacts(contacts_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(processed_contacts)

    print("Данные успешно обработаны и записаны в файл phonebook.csv")

if __name__ == "__main__":
    main()
