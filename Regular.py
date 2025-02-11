import csv
import re

def fix_contacts(contacts_list):
    for contact in contacts_list[1:]:
        full_name = contact[0] + ' ' + contact[1] + ' ' + contact[2]
        name_parts = full_name.split()

        if len(name_parts) == 3:
            contact[0] = name_parts[0]
            contact[1] = name_parts[1]
            contact[2] = name_parts[2]
        elif len(name_parts) == 2:
            contact[0] = name_parts[0]
            contact[1] = name_parts[1]
            contact[2] = ' '
        elif len(name_parts) == 1:
            contact[0] = name_parts[0]
            contact[1] = ' '
            contact[2] = ' '

    return contacts_list

def telephone(contacts_list):
    pattern_phone = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*доб\.\s*(\d+))?')

    for contact in contacts_list:
        if contact[5]:
            phone = contact[5]
            phone_1 = pattern_phone.sub(r'+7(\2)\3-\4-\5\6\7', phone)
            contact[5] = phone_1

    return contacts_list

def contacts_filter(contacts_list):
    seen = set()
    filtered_contacts = []

    for contact in contacts_list:
        new_set = (contact[0], contact[1])

        if new_set not in seen:
            filtered_contacts.append(contact)
            seen.add(new_set)

    return filtered_contacts

def split_fullname(full_name):
    parts = full_name.split()
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        return parts[0], parts[1], ''
    elif len(parts) == 1:
        return parts[0], '', ''

def format_phone(phone):
    pattern_phone = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*доб\.\s*(\d+))?')
    return pattern_phone.sub(r'+7(\2)\3-\4-\5\6', phone)


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list = fix_contacts(contacts_list)
    contacts_list = contacts_filter(contacts_list)
    contacts_list = telephone(contacts_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


