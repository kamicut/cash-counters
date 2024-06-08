import json
import requests
import time

# Embedded district data
districts_data = [
    {"id": 1, "governorateId": 1},
    {"id": 2, "governorateId": 2},
    {"id": 3, "governorateId": 2},
    {"id": 4, "governorateId": 3},
    {"id": 5, "governorateId": 4},
    {"id": 6, "governorateId": 4},
    {"id": 7, "governorateId": 4},
    {"id": 8, "governorateId": 5},
    {"id": 9, "governorateId": 5},
    {"id": 10, "governorateId": 5},
    {"id": 11, "governorateId": 5},
    {"id": 12, "governorateId": 5},
    {"id": 13, "governorateId": 5},
    {"id": 14, "governorateId": 6},
    {"id": 15, "governorateId": 6},
    {"id": 16, "governorateId": 6},
    {"id": 17, "governorateId": 6},
    {"id": 18, "governorateId": 7},
    {"id": 19, "governorateId": 7},
    {"id": 20, "governorateId": 7},
    {"id": 21, "governorateId": 7},
    {"id": 22, "governorateId": 7},
    {"id": 23, "governorateId": 7},
    {"id": 24, "governorateId": 8},
    {"id": 25, "governorateId": 8},
    {"id": 26, "governorateId": 8}
]

# Define the GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Function to fetch shop data for a given district
def fetch_shops(district_id, governorate_id, keyword=""):
    url = 'https://api.woocash.money/data/get/shops'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'keyWordSearch': keyword,
        'governorateId': governorate_id,
        'districtId': district_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        return []

# Process each district
for district in districts_data:
    district_id = district['id']
    governorate_id = district['governorateId']
    print(f"Fetching shops for district ID: {district_id}, governorate ID: {governorate_id}")
    shops = fetch_shops(district_id, governorate_id)
    for shop in shops:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [shop['longitude'], shop['latitude']]
            },
            "properties": {
                "name": shop['name'],
                "address": shop['address'],
                "phone": shop['phone'],
                "workingHours": shop['workingHours'],
                "url": shop['url'],
                "type": shop['type']
            }
        }
        geojson['features'].append(feature)
    time.sleep(1)  # To avoid hitting rate limits

# Save the combined GeoJSON to a file
with open('shops.geojson', 'w') as f:
    json.dump(geojson, f, indent=2)

print("GeoJSON file created successfully.")
