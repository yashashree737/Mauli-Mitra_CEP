import enum
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from models import (
    DindiStatus,
    DonationCategory,
    DonationStatus,
    FacilityCategory,
    JoinRequestStatus,
    ResourceNeedCategory,
    ResourceNeedStatus,
    RouteType,
    UserRole,
)


class Action(str, enum.Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


METHOD_TO_ACTION: dict[str, Action] = {
    "GET": Action.READ,
    "POST": Action.CREATE,
    "PUT": Action.UPDATE,
    "PATCH": Action.UPDATE,
    "DELETE": Action.DELETE,
}


class GeoPoint(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


T = TypeVar("T")


class ActionRequest(BaseModel, Generic[T]):
    action: Action
    id: int | None = None
    data: T | None = None


class ActionQuery(BaseModel):
    action: Action
    id: int | None = None


# --- User ---


class UserCreate(BaseModel):
    full_name: str
    phone_number: str
    role: UserRole
    dindi_id: int | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    role: UserRole | None = None
    dindi_id: int | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone_number: str
    role: UserRole
    dindi_id: int | None


# --- Dindi ---


class DindiCreate(BaseModel):
    name: str
    route_type: RouteType
    accepting_members: bool = True
    max_capacity: int
    pramukh_user_id: int | None = None
    status: DindiStatus
    village: str
    district: str
    member_count: int = 0
    extra_info: dict[str, Any] | None = None


class DindiUpdate(BaseModel):
    name: str | None = None
    route_type: RouteType | None = None
    accepting_members: bool | None = None
    max_capacity: int | None = None
    pramukh_user_id: int | None = None
    status: DindiStatus | None = None
    village: str | None = None
    district: str | None = None
    member_count: int | None = None
    extra_info: dict[str, Any] | None = None


class DindiRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    route_type: RouteType
    accepting_members: bool
    max_capacity: int
    pramukh_user_id: int | None
    status: DindiStatus
    village: str
    district: str
    member_count: int
    extra_info: dict[str, Any] | None


# --- RouteStop ---


class RouteStopCreate(BaseModel):
    dindi_id: int
    stop_name: str
    sequence_order: int
    scheduled_arrival: datetime | None = None
    scheduled_departure: datetime | None = None
    is_current_stop: bool = False
    location: GeoPoint | None = None


class RouteStopUpdate(BaseModel):
    dindi_id: int | None = None
    stop_name: str | None = None
    sequence_order: int | None = None
    scheduled_arrival: datetime | None = None
    scheduled_departure: datetime | None = None
    is_current_stop: bool | None = None
    location: GeoPoint | None = None


class RouteStopRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dindi_id: int
    stop_name: str
    sequence_order: int
    scheduled_arrival: datetime | None
    scheduled_departure: datetime | None
    is_current_stop: bool
    location: GeoPoint | None = None


# --- FacilityPoint ---


class FacilityPointCreate(BaseModel):
    name: str
    category: FacilityCategory
    verified_by_admin: bool = False
    details: str | None = None
    dindi_id: int | None = None
    phone: str | None = None
    hours: str | None = None
    location: GeoPoint | None = None


class FacilityPointUpdate(BaseModel):
    name: str | None = None
    category: FacilityCategory | None = None
    verified_by_admin: bool | None = None
    details: str | None = None
    dindi_id: int | None = None
    phone: str | None = None
    hours: str | None = None
    location: GeoPoint | None = None


class FacilityPointRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: FacilityCategory
    verified_by_admin: bool
    details: str | None
    dindi_id: int | None
    phone: str | None
    hours: str | None
    location: GeoPoint | None = None


# --- ResourceNeed ---


class ResourceNeedCreate(BaseModel):
    dindi_id: int
    category: ResourceNeedCategory
    title: str
    status: ResourceNeedStatus = ResourceNeedStatus.OPEN
    location: GeoPoint | None = None


class ResourceNeedUpdate(BaseModel):
    dindi_id: int | None = None
    category: ResourceNeedCategory | None = None
    title: str | None = None
    status: ResourceNeedStatus | None = None
    location: GeoPoint | None = None


class ResourceNeedRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dindi_id: int
    category: ResourceNeedCategory
    title: str
    status: ResourceNeedStatus
    created_at: datetime
    location: GeoPoint | None = None


# --- AmbulanceUnit ---


class AmbulanceUnitCreate(BaseModel):
    key: str
    base_location: str
    vehicle_number: str
    mems_level: str | None = None
    doctor_contacts: str | None = None
    pilot_contacts: str | None = None
    call_number: str | None = None
    district: str
    is_active: bool = True


class AmbulanceUnitUpdate(BaseModel):
    key: str | None = None
    base_location: str | None = None
    vehicle_number: str | None = None
    mems_level: str | None = None
    doctor_contacts: str | None = None
    pilot_contacts: str | None = None
    call_number: str | None = None
    district: str | None = None
    is_active: bool | None = None


class AmbulanceUnitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str
    base_location: str
    vehicle_number: str
    mems_level: str | None
    doctor_contacts: str | None
    pilot_contacts: str | None
    call_number: str | None
    district: str
    is_active: bool


# --- LiveLocationLog ---


class LiveLocationLogCreate(BaseModel):
    dindi_id: int
    timestamp: datetime | None = None
    location: GeoPoint


class LiveLocationLogUpdate(BaseModel):
    dindi_id: int | None = None
    timestamp: datetime | None = None
    location: GeoPoint | None = None


class LiveLocationLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dindi_id: int
    timestamp: datetime
    location: GeoPoint | None = None


# --- JoinRequest ---


class JoinRequestCreate(BaseModel):
    user_id: int
    dindi_id: int
    joining_date: datetime
    status: JoinRequestStatus = JoinRequestStatus.PENDING
    extra_info: dict[str, Any] | None = None


class JoinRequestUpdate(BaseModel):
    user_id: int | None = None
    dindi_id: int | None = None
    joining_date: datetime | None = None
    status: JoinRequestStatus | None = None
    extra_info: dict[str, Any] | None = None


class JoinRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    dindi_id: int
    joining_date: datetime
    status: JoinRequestStatus
    extra_info: dict[str, Any] | None


# --- DonationRequest ---


class DonationRequestCreate(BaseModel):
    dindi_id: int
    title: str
    description: str | None = None
    target_amount: int
    current_amount: int = 0
    category: DonationCategory
    status: DonationStatus = DonationStatus.PENDING
    upi_id: str | None = None
    contact_phone: str | None = None


class DonationRequestUpdate(BaseModel):
    dindi_id: int | None = None
    title: str | None = None
    description: str | None = None
    target_amount: int | None = None
    current_amount: int | None = None
    category: DonationCategory | None = None
    status: DonationStatus | None = None
    upi_id: str | None = None
    contact_phone: str | None = None


class DonationRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dindi_id: int
    title: str
    description: str | None
    target_amount: int
    current_amount: int
    category: DonationCategory
    status: DonationStatus
    upi_id: str | None
    contact_phone: str | None
