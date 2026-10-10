import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("Creating a dummy dindi...")
dindi_payload = {
    "action": "CREATE",
    "data": {
        "name": "Dummy Dindi",
        "route_type": "ON_FOOT",
        "accepting_members": True,
        "max_capacity": 100,
        "status": "PLANNED",
        "village": "Dummy Village",
        "district": "Dummy District",
        "member_count": 0
    }
}
dindi_res = client.post("/api/dindis", json=dindi_payload)
dindi_id = None
if dindi_res.status_code == 200:
    dindi_id = dindi_res.json()["id"]
    print(f"Created Dindi with ID: {dindi_id}")
else:
    print("Failed to create dindi:", dindi_res.text)

print("\nCreating dummy user...")
user_payload = {
    "action": "CREATE",
    "data": {
        "full_name": "John Doe",
        "phone_number": "8402047420",
        "role": "DINDI_PRAMUKH"
    }
}
if dindi_id is not None:
    user_payload["data"]["dindi_id"] = dindi_id

response = client.post("/api/users", json=user_payload)
print("Response status:", response.status_code)

if response.status_code == 200:
    created_user = response.json()
    user_id = created_user["id"]
    
    print(f"\nFetching user with id {user_id}...")
    fetch_response = client.get(f"/api/users?action=READ&id={user_id}")
    print("Response status:", fetch_response.status_code)
    print("Fetched User JSON:")
    print(json.dumps(fetch_response.json(), indent=2))
else:
    print("Failed to create user:", response.text)
