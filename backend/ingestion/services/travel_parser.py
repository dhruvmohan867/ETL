from datetime import datetime
from emissions.models import EmissionRecord
from .base_parser import BaseParserService


class TravelParserService(BaseParserService):
    MAX_REASONABLE_DISTANCE_KM = 20000

    def process(self):
        rows = self.read_csv()
        records = []

        for idx, row in enumerate(rows, start=1):
            origin = row.get('origin', '').strip()
            destination = row.get('destination', '').strip()
            mode = row.get('mode', '').strip()
            date_str = row.get('trip_date', '').strip()
            distance_str = row.get('distance_km', '').strip()
            raw_unit = row.get('unit', '').strip() or 'km'

            is_suspicious = False
            reasons = []

            raw_value, bad_number = self.parse_float(distance_str)
            if bad_number:
                is_suspicious = True
                reasons.append("Invalid distance value")

            if raw_value < 0:
                is_suspicious = True
                reasons.append("Negative distance")

            if raw_value > self.MAX_REASONABLE_DISTANCE_KM:
                is_suspicious = True
                reasons.append(f"Unrealistic distance: {raw_value} km")

            if not origin:
                is_suspicious = True
                reasons.append("Missing origin")

            if not destination:
                is_suspicious = True
                reasons.append("Missing destination")

            normalized_unit, normalized_value = self.normalize_unit(raw_unit, raw_value)

            reporting_date = self.parse_date(date_str)
            if not reporting_date:
                is_suspicious = True
                reasons.append("Invalid or missing date")
                reporting_date = datetime.now().date()

            category = f"{mode}: {origin} → {destination}" if mode else f"{origin} → {destination}"

            records.append(EmissionRecord(
                company=self.upload.company,
                upload=self.upload,
                row_number=idx,
                source_type='travel',
                category=category,
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
