import enum
from datetime import datetime
from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class UserRole(str, enum.Enum):
    DINDI_PRAMUKH = "DINDI_PRAMUKH"
    WALKER = "WALKER"
    VOLUNTEER = "VOLUNTEER"


class RouteType(str, enum.Enum):
    ON_FOOT = "ON_FOOT"
    VEHICLE = "VEHICLE"
    MIXED = "MIXED"


class DindiStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class FacilityCategory(str, enum.Enum):
    TOILET = "TOILET"
    NIGHT_STAY = "NIGHT_STAY"
    WATER = "WATER"
    MEDICAL = "MEDICAL"
    FOOD = "FOOD"
    OTHER = "OTHER"


class ResourceNeedCategory(str, enum.Enum):
    FOOD = "FOOD"
    WATER = "WATER"
    MEDICAL = "MEDICAL"
    TRANSPORT = "TRANSPORT"
    VOLUNTEERS = "VOLUNTEERS"
    OTHER = "OTHER"


class ResourceNeedStatus(str, enum.Enum):
    OPEN = "OPEN"
    FULFILLED = "FULFILLED"


class JoinRequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class DonationCategory(str, enum.Enum):
    FOOD = "FOOD"
    MEDICAL = "MEDICAL"
    TRANSPORT = "TRANSPORT"
    GENERAL = "GENERAL"
    OTHER = "OTHER"


class DonationStatus(str, enum.Enum):
    PENDING = "PENDING"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"


# USER

class User(Base):
    __tablename__ = "users"

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        nullable=False,
    )

    # User belongs to a Dindi.
    dindi_id: Mapped[int | None] = mapped_column(
        ForeignKey("dindis.id"),
        nullable=True,
    )

    # Relationship through User.dindi_id.
    dindi: Mapped["Dindi | None"] = relationship(
        "Dindi",
        back_populates="members",
        foreign_keys=[dindi_id],
    )

    join_requests: Mapped[list["JoinRequest"]] = relationship(
        "JoinRequest",
        back_populates="user",
    )


# DINDI

class Dindi(Base):
    __tablename__ = "dindis"

    def __str__(self):
        return self.name

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    route_type: Mapped[RouteType] = mapped_column(
        Enum(RouteType, name="route_type"),
        nullable=False,
    )

    accepting_members: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    max_capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # The Dindi's Pramukh is also a User.
    #
    # use_alter=True is important because there is also:
    #
    # users.dindi_id -> dindis.id
    #
    # This creates a circular FK relationship.
    pramukh_user_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            use_alter=True,
            name="fk_dindis_pramukh_user_id",
        ),
        nullable=True,
    )

    status: Mapped[DindiStatus] = mapped_column(
        Enum(DindiStatus, name="dindi_status"),
        nullable=False,
    )

    village: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    district: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    member_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    extra_info: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Relationships
    # Dindi -> Pramukh User
    pramukh: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[pramukh_user_id],
    )

    # Dindi -> Members
    members: Mapped[list["User"]] = relationship(
        "User",
        back_populates="dindi",
        foreign_keys="User.dindi_id",
    )

    route_stops: Mapped[list["RouteStop"]] = relationship(
        "RouteStop",
        back_populates="dindi",
    )

    facility_points: Mapped[list["FacilityPoint"]] = relationship(
        "FacilityPoint",
        back_populates="dindi",
    )

    resource_needs: Mapped[list["ResourceNeed"]] = relationship(
        "ResourceNeed",
        back_populates="dindi",
    )

    live_location_logs: Mapped[list["LiveLocationLog"]] = relationship(
        "LiveLocationLog",
        back_populates="dindi",
    )

    join_requests: Mapped[list["JoinRequest"]] = relationship(
        "JoinRequest",
        back_populates="dindi",
    )

    donation_requests: Mapped[list["DonationRequest"]] = relationship(
        "DonationRequest",
        back_populates="dindi",
    )


# ROUTE STOP

class RouteStop(Base):
    __tablename__ = "route_stops"

    def __str__(self):
        return f"{self.stop_name} (Stop {self.sequence_order})"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    dindi_id: Mapped[int] = mapped_column(
        ForeignKey("dindis.id"),
        nullable=False,
        index=True,
    )

    stop_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sequence_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    scheduled_arrival: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    scheduled_departure: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_current_stop: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # spatial_index=False is intentional.
    #
    # We create the GiST index explicitly below so Alembic
    # has one clear owner of the spatial index.
    location: Mapped[object | None] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
            spatial_index=False,
        ),
        nullable=True,
    )

    dindi: Mapped["Dindi"] = relationship(
        "Dindi",
        back_populates="route_stops",
    )

    __table_args__ = (
        Index(
            "idx_route_stops_location",
            "location",
            postgresql_using="gist",
        ),
    )

# FACILITY POINT

class FacilityPoint(Base):
    __tablename__ = "facility_points"

    def __str__(self):
        return self.name

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[FacilityCategory] = mapped_column(
        Enum(
            FacilityCategory,
            name="facility_category",
        ),
        nullable=False,
    )

    verified_by_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    dindi_id: Mapped[int | None] = mapped_column(
        ForeignKey("dindis.id"),
        nullable=True,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    hours: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    location: Mapped[object | None] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
            spatial_index=False,
        ),
        nullable=True,
    )

    dindi: Mapped["Dindi | None"] = relationship(
        "Dindi",
        back_populates="facility_points",
    )

    __table_args__ = (
        Index(
            "idx_facility_points_location",
            "location",
            postgresql_using="gist",
        ),
    )


# RESOURCE NEED


class ResourceNeed(Base):
    __tablename__ = "resource_needs"

    def __str__(self):
        return self.title

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    dindi_id: Mapped[int] = mapped_column(
        ForeignKey("dindis.id"),
        nullable=False,
        index=True,
    )

    category: Mapped[ResourceNeedCategory] = mapped_column(
        Enum(
            ResourceNeedCategory,
            name="resource_need_category",
        ),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[ResourceNeedStatus] = mapped_column(
        Enum(
            ResourceNeedStatus,
            name="resource_need_status",
        ),
        default=ResourceNeedStatus.OPEN,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    location: Mapped[object | None] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
            spatial_index=False,
        ),
        nullable=True,
    )

    dindi: Mapped["Dindi"] = relationship(
        "Dindi",
        back_populates="resource_needs",
    )

    __table_args__ = (
        Index(
            "idx_resource_needs_location",
            "location",
            postgresql_using="gist",
        ),
    )


# AMBULANCE UNIT

class AmbulanceUnit(Base):
    __tablename__ = "ambulance_units"

    def __str__(self):
        return f"{self.vehicle_number} ({self.key})"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    base_location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    vehicle_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    mems_level: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    doctor_contacts: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    pilot_contacts: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    call_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    district: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )


# LIVE LOCATION LOG


class LiveLocationLog(Base):
    __tablename__ = "live_location_logs"

    def __str__(self):
        return f"Log at {self.timestamp}"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    dindi_id: Mapped[int] = mapped_column(
        ForeignKey("dindis.id"),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    location: Mapped[object] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
            spatial_index=False,
        ),
        nullable=False,
    )

    dindi: Mapped["Dindi"] = relationship(
        "Dindi",
        back_populates="live_location_logs",
    )

    __table_args__ = (
        Index(
            "idx_live_location_logs_location",
            "location",
            postgresql_using="gist",
        ),
    )


# JOIN REQUEST

class JoinRequest(Base):
    __tablename__ = "join_requests"

    def __str__(self):
        return f"Join Request {self.id}"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    dindi_id: Mapped[int] = mapped_column(
        ForeignKey("dindis.id"),
        nullable=False,
        index=True,
    )

    joining_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[JoinRequestStatus] = mapped_column(
        Enum(
            JoinRequestStatus,
            name="join_request_status",
        ),
        default=JoinRequestStatus.PENDING,
        nullable=False,
    )

    extra_info: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="join_requests",
    )

    dindi: Mapped["Dindi"] = relationship(
        "Dindi",
        back_populates="join_requests",
    )


# DONATION REQUEST


class DonationRequest(Base):
    __tablename__ = "donation_requests"

    def __str__(self):
        return self.title

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    dindi_id: Mapped[int] = mapped_column(
        ForeignKey("dindis.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    target_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    current_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    category: Mapped[DonationCategory] = mapped_column(
        Enum(
            DonationCategory,
            name="donation_category",
        ),
        nullable=False,
    )

    status: Mapped[DonationStatus] = mapped_column(
        Enum(
            DonationStatus,
            name="donation_status",
        ),
        default=DonationStatus.PENDING,
        nullable=False,
    )

    upi_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    dindi: Mapped["Dindi"] = relationship(
        "Dindi",
        back_populates="donation_requests",
    )