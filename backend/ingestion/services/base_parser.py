import csv
import io
from datetime import datetime


class BaseParserService:
    UNIT_MAP = {
        'ltr': ('L', 1),
        'liters': ('L', 1),
        'liter': ('L', 1),
        'l': ('L', 1),
        'kl': ('L', 1000),
        'kiloliters': ('L', 1000),
        'kiloliter': ('L', 1000),
        'kwh': ('kWh', 1),
        'mwh': ('kWh', 1000),
        'gwh': ('kWh', 1000000),
        'km': ('km', 1),
        'mi': ('km', 1.60934),
        'miles': ('km', 1.60934),
    }

    DATE_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']

    def __init__(self, file_obj, upload):
        self.file_obj = file_obj
        self.upload = upload

    def read_csv(self):
        content = self.file_obj.read().decode('utf-8')
        return list(csv.DictReader(io.StringIO(content)))

    def normalize_unit(self, raw_unit, raw_value):
        if not raw_unit:
            return raw_unit, raw_value
        key = raw_unit.strip().lower()
        if key in self.UNIT_MAP:
            norm_unit, factor = self.UNIT_MAP[key]
            return norm_unit, raw_value * factor
        return raw_unit, raw_value

    def parse_date(self, date_str):
        if not date_str:
            return None
        date_str = date_str.strip()
        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None

    def parse_float(self, value_str):
        if not value_str:
            return 0.0, False
        try:
            return float(value_str.strip()), False
        except ValueError:
            return 0.0, True

    def process(self):
        raise NotImplementedError
