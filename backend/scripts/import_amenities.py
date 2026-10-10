import json
import os
import sys

# Ensure the parent directory (project root) is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import FacilityPoint, FacilityCategory
from geoalchemy2 import WKTElement

def map_category(type_str: str) -> FacilityCategory:
    if not type_str:
        return FacilityCategory.OTHER
    type_str = type_str.lower()
    if any(x in type_str for x in ['hospital', 'phc', 'icu', 'hbt', 'ambulance', 'medical', 'charanseva', 'hirkani', 'police']):
        return FacilityCategory.MEDICAL if 'police' not in type_str else FacilityCategory.OTHER
    elif 'पाणी' in type_str or 'water' in type_str:
        return FacilityCategory.WATER
    elif 'शौचालये' in type_str or 'toilet' in type_str:
        return FacilityCategory.TOILET
    elif any(x in type_str for x in ['halt', 'mukkam', 'visava', 'night']):
        return FacilityCategory.NIGHT_STAY
    elif 'food' in type_str:
        return FacilityCategory.FOOD
    else:
        return FacilityCategory.OTHER

def build_details(item: dict) -> str:
    details = []
    for key in ['palkhi', 'base', 'vehicle', 'mems', 'doctor', 'pilot', 'mo', 'toilet']:
        val = item.get(key)
        if val:
            details.append(f"{key.capitalize()}: {val}")
    return "\n".join(details)

def run():
    # The JSON is in d:/Varithon/backend/wari-amenities.json
    # __file__ is d:/Varithon/backend/maulimitra-backend-varithon/scripts/import_amenities.py
    # So 3 levels up is d:/Varithon/backend
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "wari-amenities.json")
    
    print(f"Reading from {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    db = SessionLocal()
    try:
        inserted = 0
        for item in data:
            # Prefer label, fallback to place, then to a default
            name = item.get("label")
            if not name:
                name = item.get("place")
            if not name:
                name = item.get("type", "Unknown Facility")
                
            name = name[:255]
            
            cat_str = item.get("type", "")
            category = map_category(cat_str)
            
            phone = str(item.get("call", ""))
            if phone and len(phone) > 20:
                phone = phone[:20]
                
            details = build_details(item)
            
            lat = item.get("lat")
            lng = item.get("lng")
            
            location = None
            if lat and lng:
                try:
                    lat_f = float(lat)
                    lng_f = float(lng)
                    location = WKTElement(f"POINT({lng_f} {lat_f})", srid=4326)
                except ValueError:
                    pass
                
            facility = FacilityPoint(
                name=name,
                category=category,
                verified_by_admin=True, 
                details=details if details else None,
                phone=phone if phone else None,
                location=location
            )
            db.add(facility)
            inserted += 1
        
        db.commit()
        print(f"Successfully inserted {inserted} facility points.")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run()
