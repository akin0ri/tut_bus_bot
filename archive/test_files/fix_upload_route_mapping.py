#!/usr/bin/env python3
"""
Fix for the route name mapping issue in CSV upload.

The problem: CSV files use Japanese route names but the database expects romanized names.
The solution: Add a mapping function to convert route names during upload.
"""

# Route name mapping from Japanese to romanized
ROUTE_NAME_MAPPING = {
    "八王子みなみ野駅": "minamino",
    "八王子駅南口": "hachioji", 
    "学生会館": "dormitory"
}

def convert_route_name(japanese_name):
    """Convert Japanese route name to romanized version"""
    return ROUTE_NAME_MAPPING.get(japanese_name, japanese_name)

# The fix needs to be applied in app/blueprints/admin/routes.py
# Around line 103, change:
#     route = str(row['route']) if not pd.isna(row['route']) else ''
# To:
#     route_raw = str(row['route']) if not pd.isna(row['route']) else ''
#     route = convert_route_name(route_raw)

# Also in app/blueprints/api/routes.py around line 184:
#     route=row['route'],
# To:
#     route=convert_route_name(row['route']),

# And in app/utils/csv_utils.py around line 29:
#     route=row['route'],
# To:
#     route=convert_route_name(row['route']),

print("Route name mapping fix:")
print("\nJapanese -> Romanized:")
for jp, en in ROUTE_NAME_MAPPING.items():
    print(f"  {jp} -> {en}")

print("\nFiles that need to be updated:")
print("1. app/blueprints/admin/routes.py - line ~103")
print("2. app/blueprints/api/routes.py - line ~184") 
print("3. app/utils/csv_utils.py - line ~29")
print("\nThe route name needs to be converted before storing in the database.")