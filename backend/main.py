import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

import models  # noqa: F401 — register ORM models with SQLAlchemy metadata
from admin import setup_admin
from crud import create_crud_router
from models import (
    AmbulanceUnit,
    Dindi,
    DonationRequest,
    FacilityPoint,
    JoinRequest,
    LiveLocationLog,
    ResourceNeed,
    RouteStop,
    User,
)
from schemas import (
    AmbulanceUnitCreate,
    AmbulanceUnitRead,
    AmbulanceUnitUpdate,
    DindiCreate,
    DindiRead,
    DindiUpdate,
    DonationRequestCreate,
    DonationRequestRead,
    DonationRequestUpdate,
    FacilityPointCreate,
    FacilityPointRead,
    FacilityPointUpdate,
    JoinRequestCreate,
    JoinRequestRead,
    JoinRequestUpdate,
    LiveLocationLogCreate,
    LiveLocationLogRead,
    LiveLocationLogUpdate,
    ResourceNeedCreate,
    ResourceNeedRead,
    ResourceNeedUpdate,
    RouteStopCreate,
    RouteStopRead,
    RouteStopUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)

app = FastAPI(title="Mauli Mitra API", version="1.0.0")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
)

app.include_router(
    create_crud_router(
        prefix="/users",
        tag="users",
        model=User,
        create_schema=UserCreate,
        update_schema=UserUpdate,
        read_schema=UserRead,
    )
)
app.include_router(
    create_crud_router(
        prefix="/dindis",
        tag="dindis",
        model=Dindi,
        create_schema=DindiCreate,
        update_schema=DindiUpdate,
        read_schema=DindiRead,
    )
)
app.include_router(
    create_crud_router(
        prefix="/route-stops",
        tag="route-stops",
        model=RouteStop,
        create_schema=RouteStopCreate,
        update_schema=RouteStopUpdate,
        read_schema=RouteStopRead,
        location_fields={"location"},
        order_by=lambda: RouteStop.sequence_order,
    )
)
app.include_router(
    create_crud_router(
        prefix="/facility-points",
        tag="facility-points",
        model=FacilityPoint,
        create_schema=FacilityPointCreate,
        update_schema=FacilityPointUpdate,
        read_schema=FacilityPointRead,
        location_fields={"location"},
    )
)
app.include_router(
    create_crud_router(
        prefix="/resource-needs",
        tag="resource-needs",
        model=ResourceNeed,
        create_schema=ResourceNeedCreate,
        update_schema=ResourceNeedUpdate,
        read_schema=ResourceNeedRead,
        location_fields={"location"},
        order_by=lambda: ResourceNeed.created_at.desc(),
    )
)
app.include_router(
    create_crud_router(
        prefix="/ambulance-units",
        tag="ambulance-units",
        model=AmbulanceUnit,
        create_schema=AmbulanceUnitCreate,
        update_schema=AmbulanceUnitUpdate,
        read_schema=AmbulanceUnitRead,
    )
)
app.include_router(
    create_crud_router(
        prefix="/live-location-logs",
        tag="live-location-logs",
        model=LiveLocationLog,
        create_schema=LiveLocationLogCreate,
        update_schema=LiveLocationLogUpdate,
        read_schema=LiveLocationLogRead,
        location_fields={"location"},
        order_by=lambda: LiveLocationLog.timestamp.desc(),
    )
)
app.include_router(
    create_crud_router(
        prefix="/join-requests",
        tag="join-requests",
        model=JoinRequest,
        create_schema=JoinRequestCreate,
        update_schema=JoinRequestUpdate,
        read_schema=JoinRequestRead,
    )
)
app.include_router(
    create_crud_router(
        prefix="/donation-requests",
        tag="donation-requests",
        model=DonationRequest,
        create_schema=DonationRequestCreate,
        update_schema=DonationRequestUpdate,
        read_schema=DonationRequestRead,
    )
)

setup_admin(app)


@app.get("/health")
def health_check():
    return {"status": "ok"}
