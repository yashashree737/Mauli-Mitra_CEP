# Wari Seva Project - Seed File (Pseudocode)

## 1. Data Models
This section outlines the pseudocode for the underlying data structures.

**1. User Model**
- Properties: id (Integer), full_name (String), phone_number (String), role (Enum: DINDI_PRAMUKH, WALKER, VOLUNTEER), dindi_id (Foreign Key)

**2. Dindi Model**
- Properties: id (Integer), name (String), route_type (Enum), accepting_members (Boolean), max_capacity (Integer), pramukh_user_id (Foreign Key), status (Enum), village (String), district (String), member_count (Integer), extra_info (JSON)

**3. RouteStop Model**
- Properties: id (Integer), dindi_id (Foreign Key), stop_name (String), sequence_order (Integer), scheduled_arrival (DateTime), scheduled_departure (DateTime), is_current_stop (Boolean), location (Point/Geometry)

**4. FacilityPoint Model**
- Properties: id (Integer), name (String), category (Enum: TOILET, NIGHT_STAY, etc.), verified_by_admin (Boolean), details (Text), dindi_id (Foreign Key), phone (String), hours (String), location (Point/Geometry)

**5. ResourceNeed Model**
- Properties: id (Integer), dindi_id (Foreign Key), category (Enum), title (String), status (Enum: OPEN, FULFILLED), created_at (DateTime), location (Point/Geometry)

**6. AmbulanceUnit Model**
- Properties: id (Integer), key (String), base_location (String), vehicle_number (String), mems_level (String), doctor_contacts (Text), pilot_contacts (Text), call_number (String), district (String), is_active (Boolean)

**7. LiveLocationLog Model**
- Properties: id (Integer), dindi_id (Foreign Key), timestamp (DateTime), location (Point/Geometry)

**8. JoinRequest Model**
- Properties: id (Integer), user_id (Foreign Key), dindi_id (Foreign Key), joining_date (DateTime), status (Enum: PENDING, ACCEPTED, REJECTED), extra_info (JSON)

**9. DonationRequest Model**
- Properties: id (Integer), dindi_id (Foreign Key), title (String), description (Text), target_amount (Integer), current_amount (Integer), category (Enum), status (Enum: PENDING, FULFILLED, CANCELLED), upi_id (String), contact_phone (String)

---

## 2. API Endpoints
The backend exposes 9 primary endpoints (one for each model), offering CRUD operations.

**1. `/api/users`**
- Action: CREATE, READ, UPDATE, DELETE

**2. `/api/dindis`**
- Action: CREATE, READ, UPDATE, DELETE

**3. `/api/route-stops`**
- Action: CREATE, READ, UPDATE, DELETE

**4. `/api/facility-points`**
- Action: CREATE, READ, UPDATE, DELETE

**5. `/api/resource-needs`**
- Action: CREATE, READ, UPDATE, DELETE

**6. `/api/ambulance-units`**
- Action: CREATE, READ, UPDATE, DELETE

**7. `/api/live-location-logs`**
- Action: CREATE, READ, UPDATE, DELETE

**8. `/api/join-requests`**
- Action: CREATE, READ, UPDATE, DELETE

**9. `/api/donation-requests`**
- Action: CREATE, READ, UPDATE, DELETE

---

## 3. Admin Panel
The admin dashboard is structured to manage the above data models seamlessly.

- **Authentication**: Secured via Admin Username/Password.
- **People Management**: 
  - `UserAdmin`: View, search, and edit users.
  - `JoinRequestAdmin`: Manage and approve/reject pending join requests.
- **Dindis Management**:
  - `DindiAdmin`: Manage Dindis, verify their status, edit extra info JSONs.
  - `RouteStopAdmin`: Manage schedule and geolocations (lat/lng points) of halts.
  - `LiveLocationLogAdmin`: View logs of live location pings.
- **Facilities & Aid Management**:
  - `FacilityPointAdmin`: Manage toilets, medical camps, water points.
  - `ResourceNeedAdmin`: Oversee active resource needs for Dindis.
  - `AmbulanceUnitAdmin`: Manage the 108/102 fleet directory and active status.
  - `DonationRequestAdmin`: Track and manage donation campaigns for Dindis.

---

## 4. Project Architecture
Carried over from the earlier reference project (FastAPI + SQLAlchemy + Alembic), the backend follows a flat, single-service layout — no nested `app/` package, everything sits at the project root for simplicity.

```
wari-seva-backend/
├── alembic/                  # Migration environment (see Section 5)
│   ├── versions/              # Auto-generated migration scripts
│   ├── README
│   ├── env.py                 # Alembic runtime config (DB URL, target metadata)
│   └── script.py.mako         # Template used to generate new revision files
├── scripts/                   # One-off / maintenance scripts (seeding, backfills, etc.)
├── .env.example                # Template for required environment variables
├── .gitignore
├── admin.py                   # Admin panel routes/views (Section 3 above)
├── alembic.ini                 # Alembic CLI config, points to alembic/env.py
├── curl_commands.txt           # Sample curl requests for manually exercising each endpoint
├── database.py                 # DB engine/session setup (SQLAlchemy engine, SessionLocal, Base)
├── deployment.md                # Deployment notes (VPS setup, process manager, env vars)
├── main.py                     # App entrypoint — FastAPI app instance, router includes
├── models.py                   # SQLAlchemy ORM models (Section 1 above — User, Dindi, RouteStop, etc.)
├── requirements.txt
└── schemas.py                  # Pydantic request/response schemas for the 9 endpoints
```

**Notes on adapting this structure to Wari Seva:**
- `models.py` will hold all 9 models from Section 1 (consider splitting into `models/` package once the file grows past ~300–400 lines, mirroring model groupings: people, dindis, facilities/aid).
- `schemas.py` should define separate Create / Update / Read (response) schemas per model, especially for `Dindi` and `RouteStop` where `extra_info` (JSON) and `location` (Point/Geometry) need custom serializers.
- `database.py` needs a PostGIS-aware engine setup if `location` fields use PostGIS `Point` types (recommended given RouteStop, FacilityPoint, ResourceNeed, and LiveLocationLog all store geolocation).
- `admin.py` implements the panels listed in Section 3 (`UserAdmin`, `DindiAdmin`, `AmbulanceUnitAdmin`, etc.).
- `curl_commands.txt` should be kept up to date with one working example per endpoint in Section 2, useful for manual QA during the Wari season crunch.

---

## 5. Alembic Migration Management
Schema changes are managed through Alembic rather than `create_all()`, so every change to `models.py` is versioned and reproducible across dev, staging, and the VPS.

**Setup**
- `alembic.ini` at the project root holds the CLI configuration and points `script_location` at the `alembic/` folder. The actual DB connection string is read from the environment (via `.env`) inside `alembic/env.py` rather than hardcoded in `alembic.ini`, so the same config works across environments.
- `alembic/env.py` imports `Base` from `database.py` and all models from `models.py` so `target_metadata = Base.metadata` picks up every table for autogeneration.
- `alembic/script.py.mako` is the template used to scaffold each new revision file (`upgrade()` / `downgrade()` functions).
- `alembic/versions/` accumulates one file per revision, each linked to the previous via `down_revision`, forming a linear migration history.

**Day-to-day workflow**
1. Modify `models.py` (e.g., add a field to `DonationRequest`, or a new `AmbulanceUnit` column).
2. Autogenerate a revision:
   ```
   alembic revision --autogenerate -m "add upi_id to donation_request"
   ```
3. Review the generated script in `alembic/versions/` — autogenerate doesn't always catch everything (e.g., Enum changes, Point/Geometry column types via PostGIS need manual review).
4. Apply it:
   ```
   alembic upgrade head
   ```
5. To roll back one step during testing:
   ```
   alembic downgrade -1
   ```

**Conventions for this project**
- One revision per logical change — don't bundle unrelated model changes (e.g., keep `Dindi` status changes separate from `AmbulanceUnit` additions) so rollbacks stay safe and targeted.
- Since several models carry `Point/Geometry` columns (RouteStop, FacilityPoint, ResourceNeed, LiveLocationLog), the PostGIS extension (`CREATE EXTENSION postgis`) should be added as an explicit `op.execute(...)` step in the first migration, before any geometry column is created.
- Enum types (`route_type`, `status`, `category`, etc.) should be created/altered explicitly in migrations — Alembic's autogenerate support for enum value changes is limited, especially on Postgres.
- `deployment.md` should document running `alembic upgrade head` as a required step in the VPS deploy process, before the app process restarts.
