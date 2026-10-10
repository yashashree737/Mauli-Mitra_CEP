import sys
import random
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from main import app
from schemas import (
    UserRole, RouteType, DindiStatus, ResourceNeedCategory,
    ResourceNeedStatus, JoinRequestStatus, DonationCategory, DonationStatus
)

client = TestClient(app)

def create_entries():
    run_id = str(random.randint(1000, 9999))
    print(f"Creating Users (run {run_id})...")
    users_data = [
        {"full_name": "Ramesh Kumar", "phone_number": f"912345{run_id}", "role": UserRole.DINDI_PRAMUKH.value},
        {"full_name": "Suresh Patil", "phone_number": f"912346{run_id}", "role": UserRole.WALKER.value},
        {"full_name": "Anjali Deshmukh", "phone_number": f"912347{run_id}", "role": UserRole.VOLUNTEER.value},
        {"full_name": "Priya Sharma", "phone_number": f"912348{run_id}", "role": UserRole.WALKER.value},
        {"full_name": "Ganesh Joshi", "phone_number": f"912349{run_id}", "role": UserRole.DINDI_PRAMUKH.value},
    ]
    user_ids = []
    for data in users_data:
        response = client.post("/users", json={"action": "CREATE", "data": data})
        if response.status_code == 200:
            user_ids.append(response.json()["id"])
        else:
            print(f"Failed to create user: {response.text}")

    print("Creating Dindis...")
    dindis_data = [
        {"name": f"Sant Dnyaneshwar Maharaj Palkhi {run_id}", "route_type": RouteType.ON_FOOT.value, "max_capacity": 1000, "status": DindiStatus.ACTIVE.value, "village": "Alandi", "district": "Pune"},
        {"name": f"Sant Tukaram Maharaj Palkhi {run_id}", "route_type": RouteType.ON_FOOT.value, "max_capacity": 1500, "status": DindiStatus.ACTIVE.value, "village": "Dehu", "district": "Pune"},
        {"name": f"Sant Gajanan Maharaj Palkhi {run_id}", "route_type": RouteType.VEHICLE.value, "max_capacity": 500, "status": DindiStatus.PLANNED.value, "village": "Shegaon", "district": "Buldhana"},
        {"name": f"Sant Sopankaka Palkhi {run_id}", "route_type": RouteType.MIXED.value, "max_capacity": 200, "status": DindiStatus.COMPLETED.value, "village": "Saswad", "district": "Pune"},
        {"name": f"Sant Eknath Maharaj Palkhi {run_id}", "route_type": RouteType.ON_FOOT.value, "max_capacity": 800, "status": DindiStatus.ACTIVE.value, "village": "Paithan", "district": "Aurangabad"},
    ]
    dindi_ids = []
    for i, data in enumerate(dindis_data):
        if i < len(user_ids):
            data["pramukh_user_id"] = user_ids[i]
        response = client.post("/dindis", json={"action": "CREATE", "data": data})
        if response.status_code == 200:
            dindi_ids.append(response.json()["id"])
        else:
            print(f"Failed to create dindi: {response.text}")

    if not dindi_ids:
        print("No Dindis created, exiting early.")
        return

    print("Creating RouteStops...")
    route_stops_data = [
        {"stop_name": "Alandi Temple", "sequence_order": 1, "is_current_stop": False, "location": {"latitude": 18.6756, "longitude": 73.8938}},
        {"stop_name": "Pune Bhavani Peth", "sequence_order": 2, "is_current_stop": True, "location": {"latitude": 18.5130, "longitude": 73.8643}},
        {"stop_name": "Saswad", "sequence_order": 3, "is_current_stop": False, "location": {"latitude": 18.3414, "longitude": 74.0287}},
        {"stop_name": "Jejuri", "sequence_order": 4, "is_current_stop": False, "location": {"latitude": 18.2771, "longitude": 74.1593}},
        {"stop_name": "Pandharpur Vitthal Temple", "sequence_order": 5, "is_current_stop": False, "location": {"latitude": 17.6766, "longitude": 75.3262}},
    ]
    for i, data in enumerate(route_stops_data):
        data["dindi_id"] = dindi_ids[i % len(dindi_ids)]
        # Add some scheduled times
        data["scheduled_arrival"] = (datetime.now(timezone.utc) + timedelta(days=i)).isoformat()
        response = client.post("/route-stops", json={"action": "CREATE", "data": data})
        if response.status_code != 200:
            print(f"Failed to create route stop: {response.text}")

    print("Creating ResourceNeeds...")
    needs_data = [
        {"category": ResourceNeedCategory.FOOD.value, "title": "Dinner for 500 warkaris"},
        {"category": ResourceNeedCategory.WATER.value, "title": "Drinking water tanker"},
        {"category": ResourceNeedCategory.MEDICAL.value, "title": "First aid supplies"},
        {"category": ResourceNeedCategory.TRANSPORT.value, "title": "Vehicle for luggage"},
        {"category": ResourceNeedCategory.VOLUNTEERS.value, "title": "10 volunteers for crowd control"},
    ]
    for i, data in enumerate(needs_data):
        data["dindi_id"] = dindi_ids[i % len(dindi_ids)]
        data["location"] = {"latitude": 18.5 + random.uniform(0, 0.5), "longitude": 73.8 + random.uniform(0, 0.5)}
        response = client.post("/resource-needs", json={"action": "CREATE", "data": data})
        if response.status_code != 200:
            print(f"Failed to create resource need: {response.text}")

    print("Creating AmbulanceUnits...")
    ambulances_data = [
        {"key": f"AMB_PUN_01_{run_id}", "base_location": "Pune Station", "vehicle_number": "MH 12 AB 1234", "district": "Pune"},
        {"key": f"AMB_PUN_02_{run_id}", "base_location": "Alandi", "vehicle_number": "MH 14 CD 5678", "district": "Pune", "mems_level": "ALS"},
        {"key": f"AMB_SOL_01_{run_id}", "base_location": "Pandharpur", "vehicle_number": "MH 13 EF 9012", "district": "Solapur"},
        {"key": f"AMB_SAT_01_{run_id}", "base_location": "Satara", "vehicle_number": "MH 11 GH 3456", "district": "Satara", "doctor_contacts": "Dr. Joshi 9876543210"},
        {"key": f"AMB_AUR_01_{run_id}", "base_location": "Paithan", "vehicle_number": "MH 20 IJ 7890", "district": "Aurangabad"},
    ]
    for data in ambulances_data:
        response = client.post("/ambulance-units", json={"action": "CREATE", "data": data})
        if response.status_code != 200:
            print(f"Failed to create ambulance unit: {response.text}")

    print("Creating LiveLocationLogs...")
    for i in range(5):
        data = {
            "dindi_id": dindi_ids[i % len(dindi_ids)],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "location": {"latitude": 18.5 + random.uniform(-0.1, 0.1), "longitude": 73.8 + random.uniform(-0.1, 0.1)}
        }
        response = client.post("/live-location-logs", json={"action": "CREATE", "data": data})
        if response.status_code != 200:
            print(f"Failed to create live location log: {response.text}")

    print("Creating JoinRequests...")
    for i in range(5):
        if not user_ids:
            break
        data = {
            "user_id": user_ids[i % len(user_ids)],
            "dindi_id": dindi_ids[i % len(dindi_ids)],
            "joining_date": (datetime.now(timezone.utc) + timedelta(days=random.randint(1, 5))).isoformat(),
            "status": JoinRequestStatus.PENDING.value
        }
        response = client.post("/join-requests", json={"action": "CREATE", "data": data})
        if response.status_code != 200:
            print(f"Failed to create join request: {response.text}")

    print("Creating DonationRequests...")
    donations_data = [
        {"title": "Food for 1000 people", "target_amount": 50000, "category": DonationCategory.FOOD.value},
        {"title": "Medical camp supplies", "target_amount": 20000, "category": DonationCategory.MEDICAL.value},
        {"title": "Transport expenses", "target_amount": 10000, "category": DonationCategory.TRANSPORT.value},
        {"title": "General Dindi Fund", "target_amount": 100000, "category": DonationCategory.GENERAL.value},
        {"title": "Water distribution", "target_amount": 5000, "category": DonationCategory.OTHER.value},
    ]
    for i, data in enumerate(donations_data):
        data["dindi_id"] = dindi_ids[i % len(dindi_ids)]
        response = client.post("/donation-requests", json={"action": "CREATE", "data": data})
        if response.status_code != 200:
            print(f"Failed to create donation request: {response.text}")
            
    print("Done!")

if __name__ == "__main__":
    create_entries()
