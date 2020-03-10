import csv
from collections import Counter


def get_dict(file_name):
    lines = read_csv(file_name)
    field_names = next(lines)
    for line in lines:
        yield dict(zip(field_names, line))


def read_csv(file_name):
    with open(file_name) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        yield from reader


def combine(primary_info, other_info):
    for entry in primary_info:
        for other_entry in other_info:
            other_data = next(other_entry)
            if other_data.get('ssn') == entry.get('ssn'):
                entry.update(other_data)
            else:
                raise Exception('Unknown SSN')
        yield entry


personal_info = get_dict('personal_info.csv')
vehicles = get_dict('vehicles.csv')
employment = get_dict('employment.csv')
update_status = get_dict('update_status.csv')

data = combine(personal_info, [vehicles, employment, update_status])
tickets_by_make = Counter()
for entry in data:
    tickets_by_make.update({entry['vehicle_make']: 1})

print(tickets_by_make)
