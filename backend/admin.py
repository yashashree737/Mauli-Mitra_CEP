import os

from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from database import engine
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


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        admin_user = os.getenv("ADMIN_USERNAME", "admin")
        admin_pass = os.getenv("ADMIN_PASSWORD", "admin")
        if username == admin_user and password == admin_pass:
            request.session.update({"authenticated": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("authenticated", False) is True


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    category = "Accounts"
    column_list = [User.id, User.full_name, User.phone_number, User.role, User.dindi]
    column_searchable_list = [User.full_name, User.phone_number]
    form_columns = [User.full_name, User.phone_number, User.role, User.dindi]


class JoinRequestAdmin(ModelView, model=JoinRequest):
    name = "Join Request"
    name_plural = "Join Requests"
    icon = "fa-solid fa-user-plus"
    category = "Accounts"
    column_list = [
        JoinRequest.id,
        JoinRequest.user,
        JoinRequest.dindi,
        JoinRequest.joining_date,
        JoinRequest.status,
    ]
    column_searchable_list = [JoinRequest.status]
    form_columns = [
        JoinRequest.user,
        JoinRequest.dindi,
        JoinRequest.joining_date,
        JoinRequest.status,
        JoinRequest.extra_info,
    ]


class DindiAdmin(ModelView, model=Dindi):
    name = "Dindi"
    name_plural = "Dindis"
    icon = "fa-solid fa-users-line"
    category = "Dindi Management"
    column_list = [
        Dindi.id,
        Dindi.name,
        Dindi.route_type,
        Dindi.status,
        Dindi.village,
        Dindi.district,
        Dindi.member_count,
        Dindi.accepting_members,
    ]
    column_searchable_list = [Dindi.name, Dindi.village, Dindi.district]
    form_columns = [
        Dindi.name,
        Dindi.route_type,
        Dindi.accepting_members,
        Dindi.max_capacity,
        Dindi.pramukh,
        Dindi.status,
        Dindi.village,
        Dindi.district,
        Dindi.member_count,
        Dindi.extra_info,
    ]


class RouteStopAdmin(ModelView, model=RouteStop):
    name = "Route Stop"
    name_plural = "Route Stops"
    icon = "fa-solid fa-location-dot"
    category = "Dindi Management"
    column_list = [
        RouteStop.id,
        RouteStop.dindi,
        RouteStop.stop_name,
        RouteStop.sequence_order,
        RouteStop.is_current_stop,
    ]
    column_searchable_list = [RouteStop.stop_name]
    form_columns = [
        RouteStop.dindi,
        RouteStop.stop_name,
        RouteStop.sequence_order,
        RouteStop.scheduled_arrival,
        RouteStop.scheduled_departure,
        RouteStop.is_current_stop,
        RouteStop.location,
    ]


class LiveLocationLogAdmin(ModelView, model=LiveLocationLog):
    name = "Live Location Log"
    name_plural = "Live Location Logs"
    icon = "fa-solid fa-map-location-dot"
    category = "Dindi Management"
    column_list = [
        LiveLocationLog.id,
        LiveLocationLog.dindi,
        LiveLocationLog.timestamp,
    ]
    form_columns = [
        LiveLocationLog.dindi,
        LiveLocationLog.timestamp,
        LiveLocationLog.location,
    ]


class FacilityPointAdmin(ModelView, model=FacilityPoint):
    name = "Facility Point"
    name_plural = "Facility Points"
    icon = "fa-solid fa-hospital"
    category = "Facilities & Resources"
    column_list = [
        FacilityPoint.id,
        FacilityPoint.name,
        FacilityPoint.category,
        FacilityPoint.verified_by_admin,
        FacilityPoint.dindi,
    ]
    column_searchable_list = [FacilityPoint.name, FacilityPoint.category]
    form_columns = [
        FacilityPoint.name,
        FacilityPoint.category,
        FacilityPoint.verified_by_admin,
        FacilityPoint.details,
        FacilityPoint.dindi,
        FacilityPoint.phone,
        FacilityPoint.hours,
        FacilityPoint.location,
    ]


class ResourceNeedAdmin(ModelView, model=ResourceNeed):
    name = "Resource Need"
    name_plural = "Resource Needs"
    icon = "fa-solid fa-hand-holding-hand"
    category = "Facilities & Resources"
    column_list = [
        ResourceNeed.id,
        ResourceNeed.dindi,
        ResourceNeed.title,
        ResourceNeed.category,
        ResourceNeed.status,
        ResourceNeed.created_at,
    ]
    column_searchable_list = [ResourceNeed.title, ResourceNeed.status]
    form_columns = [
        ResourceNeed.dindi,
        ResourceNeed.title,
        ResourceNeed.category,
        ResourceNeed.status,
        ResourceNeed.location,
    ]


class AmbulanceUnitAdmin(ModelView, model=AmbulanceUnit):
    name = "Ambulance Unit"
    name_plural = "Ambulance Units"
    icon = "fa-solid fa-truck-medical"
    category = "Facilities & Resources"
    column_list = [
        AmbulanceUnit.id,
        AmbulanceUnit.key,
        AmbulanceUnit.vehicle_number,
        AmbulanceUnit.district,
        AmbulanceUnit.is_active,
    ]
    column_searchable_list = [
        AmbulanceUnit.key,
        AmbulanceUnit.vehicle_number,
        AmbulanceUnit.district,
    ]


class DonationRequestAdmin(ModelView, model=DonationRequest):
    name = "Donation Request"
    name_plural = "Donation Requests"
    icon = "fa-solid fa-hand-holding-dollar"
    category = "Donations"
    column_list = [
        DonationRequest.id,
        DonationRequest.dindi,
        DonationRequest.title,
        DonationRequest.category,
        DonationRequest.status,
        DonationRequest.target_amount,
        DonationRequest.current_amount,
    ]
    column_searchable_list = [DonationRequest.title, DonationRequest.status]
    form_columns = [
        DonationRequest.dindi,
        DonationRequest.title,
        DonationRequest.description,
        DonationRequest.target_amount,
        DonationRequest.current_amount,
        DonationRequest.category,
        DonationRequest.status,
        DonationRequest.upi_id,
        DonationRequest.contact_phone,
    ]


def setup_admin(app: FastAPI) -> None:
    secret_key = os.getenv("SECRET_KEY", "change-me-in-production")
    authentication_backend = AdminAuth(secret_key=secret_key)
    admin = Admin(app, engine, authentication_backend=authentication_backend, title="MauliMitra Admin Panel")

    admin.add_view(UserAdmin)
    admin.add_view(JoinRequestAdmin)
    admin.add_view(DindiAdmin)
    admin.add_view(RouteStopAdmin)
    admin.add_view(LiveLocationLogAdmin)
    admin.add_view(FacilityPointAdmin)
    admin.add_view(ResourceNeedAdmin)
    admin.add_view(AmbulanceUnitAdmin)
    admin.add_view(DonationRequestAdmin)
