from datetime import datetime
from emissions.models import EmissionRecord
from .base_parser import BaseParserService


class UtilityParserService(BaseParserService):
    def process(self):
        rows = self.read_csv()
        records = []
        values_for_spike = []

        for row in rows:
            val, _ = self.parse_float(row.get('kwh_consumed', '').strip())
            if val > 0:
                values_for_spike.append(val)

        median_val = sorted(values_for_spike)[len(values_for_spike) // 2] if values_for_spike else 0

        for idx, row in enumerate(rows, start=1):
            meter_id = row.get('meter_id', '').strip()
            provider = row.get('provider', '').strip()
            raw_unit = row.get('unit', '').strip() or 'kWh'
            date_str = row.get('reading_date', '').strip()
            quantity_str = row.get('kwh_consumed', '').strip()

            is_suspicious = False
            reasons = []

            raw_value, bad_number = self.parse_float(quantity_str)
            if bad_number:
                is_suspicious = True
                reasons.append("Invalid consumption value")

            if raw_value < 0:
                is_suspicious = True
                reasons.append("Negative consumption")

            if raw_value == 0 and not bad_number:
                is_suspicious = True
                reasons.append("Zero consumption reading")

            if median_val > 0 and raw_value > median_val * 10:
                is_suspicious = True
                reasons.append(f"Usage spike: {raw_value} vs median {median_val}")

            if not meter_id:
                is_suspicious = True
                reasons.append("Missing meter ID")

            normalized_unit, normalized_value = self.normalize_unit(raw_unit, raw_value)

            reporting_date = self.parse_date(date_str)
            if not reporting_date:
                is_suspicious = True
                reasons.append("Invalid or missing date")
                reporting_date = datetime.now().date()

            category = f"{provider} — {meter_id}" if provider and meter_id else provider or meter_id or "Unknown"

            records.append(EmissionRecord(
                company=self.upload.company,
                upload=self.upload,
                row_number=idx,
                source_type='utility',
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
