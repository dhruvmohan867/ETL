#  Emissions Ingestion Platform

Django REST + React prototype for ingesting fuel, electricity, and travel data from enterprise sources, normalizing it, flagging suspicious rows, and providing an analyst review workflow before audit.

## Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Backend runs at `http://localhost:8000`, frontend at `http://localhost:5173`.

## Data Sources

| Source | Format | Scope | Sample File |
|---|---|---|---|
| SAP Fuel/Procurement | IDoc flat-file CSV (WERKS, MATNR, MENGE, MEINS, BUDAT) | Scope 1 | `sample_sap.csv` |
| Utility Electricity | Portal CSV (account, meter, billing period, consumption) | Scope 2 | `sample_utility.csv` |
| Corporate Travel | Concur-style CSV (booking_ref, IATA codes, travel class) | Scope 3 | `sample_travel.csv` |

## API Endpoints

| Method | URL | Purpose |
|---|---|---|
| POST | `/api/uploads/sap_fuel/` | Upload SAP fuel data |
| POST | `/api/uploads/utility/` | Upload utility data |
| POST | `/api/uploads/travel/` | Upload travel data |
| GET | `/api/emissions/` | List records (filterable) |
| GET | `/api/emissions/dashboard/` | Aggregated stats |
| GET/POST | `/api/reviews/` | Review decisions |
| GET | `/api/audit-logs/` | Audit trail |

## Documentation

- [MODEL.md](MODEL.md) — Data model rationale
- [DECISIONS.md](DECISIONS.md) — Ambiguity resolutions
- [TRADEOFFS.md](TRADEOFFS.md) — What was deliberately not built
- [SOURCES.md](SOURCES.md) — Source research and sample data design
