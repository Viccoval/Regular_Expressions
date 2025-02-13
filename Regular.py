import csv
import re

def fix_contacts(contacts_list):
    for contact in contacts_list[1:]:
        name_parts = " ".join(contact[:3]).split()
        contact[:3] = (name_parts + [""] * 3)[:3]
    return contacts_list


def format_phone(phone):
    pattern_phone = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*доб\.\s*(\d+))?')
    match = pattern_phone.search(phone)
    if match:
        formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        return f"{formatted_phone} {match.group(7)}" if match.group(7) else formatted_phone

    return phone.strip()


def process_phones(contacts_list):
    for contact in contacts_list:
        if contact[5]:
            contact[5] = format_phone(contact[5])
    return contacts_list


def merge_contacts(existing, new):
    return [new[i] if not existing[i] else existing[i] for i in range(len(existing))]


def contacts_filter(contacts_list):

    unique_contacts = {}
    for contact in contacts_list:
        key = (contact[0], contact[1])
        if key in unique_contacts:
            unique_contacts[key] = merge_contacts(unique_contacts[key], contact)
        else:
            unique_contacts[key] = contact
    return list(unique_contacts.values())


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list = fix_contacts(contacts_list)
    contacts_list = contacts_filter(contacts_list)
    contacts_list = process_phones(contacts_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


