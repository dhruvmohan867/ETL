from datetime import datetime
from emissions.models import EmissionRecord
from .base_parser import BaseParserService


class SAPParserService(BaseParserService):
    def process(self):
        rows = self.read_csv()
        records = []

        for idx, row in enumerate(rows, start=1):
            source_type = row.get('source_type', '').strip()
            category = row.get('category', '').strip()
            raw_unit = row.get('unit', '').strip()
            date_str = row.get('date', '').strip()
            quantity_str = row.get('quantity', '').strip()

            is_suspicious = False
            reasons = []

            raw_value, bad_number = self.parse_float(quantity_str)
            if bad_number:
                is_suspicious = True
                reasons.append("Invalid quantity format")

            if raw_value < 0:
                is_suspicious = True
                reasons.append("Negative quantity")

            if not raw_unit:
                is_suspicious = True
                reasons.append("Missing unit")

            normalized_unit, normalized_value = self.normalize_unit(raw_unit, raw_value)

            reporting_date = self.parse_date(date_str)
            if not reporting_date:
                is_suspicious = True
                reasons.append("Invalid or missing date")
                reporting_date = datetime.now().date()

            records.append(EmissionRecord(
                company=self.upload.company,
                upload=self.upload,
                row_number=idx,
                source_type='sap_fuel',
                category=category or source_type,
                raw_value=raw_value,
                normalized_value=normalized_value,
                raw_unit=raw_unit,
                normalized_unit=normalized_unit,
                reporting_date=reporting_date,
                is_suspicious=is_suspicious,
                suspicious_reason="; ".join(reasons),
            ))

        EmissionRecord.objects.bulk_create(records)

        suspicious_count = sum(1 for r in records if r.is_suspicious)
        self.upload.row_count = len(records)
        self.upload.suspicious_count = suspicious_count
        self.upload.status = 'completed'
        self.upload.save()

        return len(records)
