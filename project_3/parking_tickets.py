from datetime import datetime
import re
from collections import namedtuple, defaultdict, Counter

from typing import List


class ParkingTicketsIterator:
    def __init__(self, file):
        self.file = file

    def read_file(self):
        with open(self.file) as f:
            print("Open file")
            Ticket = namedtuple('Ticket', [c.replace(' ', '_') for c in f.readline().strip().split(',')])

            for line in f:
                parsed_line = self._convert_line(line)
                if all(parsed_line):
                    try:
                        yield Ticket(*parsed_line)
                    except:
                        print(parsed_line)

    def _convert_line(self, line: str) -> List[str]:
        line = line.strip().split(',')
        return [self._convert(value) for value in line]

    def _convert_int(self, value: str) -> int:
        if re.match(pattern='^\d+$', string=value):
            return int(value)

    def _convert_date(self, value: str) -> datetime:
        if re.match(pattern='^\d{1,2}/\d{1,2}/\d{4}$', string=value):
            return datetime.strptime(value, '%m/%d/%Y')

    def _convert(self, value: str):
        output = self._convert_int(value)
        if not output:
            output = self._convert_date(value)
        return output or value


parking_tickets_iterator = ParkingTicketsIterator('nyc_parking_tickets_extract.csv').read_file()
violations_by_make = defaultdict(int)
for ticket in parking_tickets_iterator:
    make = ticket.Vehicle_Make
    violations_by_make[make] += 1
print(violations_by_make)

parking_tickets_iterator = ParkingTicketsIterator('nyc_parking_tickets_extract.csv').read_file()
violations_by_make = Counter(x.Vehicle_Make for x in parking_tickets_iterator)
print(violations_by_make)
