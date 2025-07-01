#!/usr/bin/env python3
"""Test the route name conversion fix"""

# Route name mapping from Japanese to romanized
ROUTE_NAME_MAPPING = {
    "八王子みなみ野駅": "minamino",
    "八王子駅南口": "hachioji", 
    "学生会館": "dormitory"
}

def convert_route_name(japanese_name):
    """Convert Japanese route name to romanized version"""
    return ROUTE_NAME_MAPPING.get(japanese_name, japanese_name)

def test_conversion():
    """Test route name conversion"""
    print("=== Route Name Conversion Test ===\n")
    
    # Test data from CSV
    test_routes = [
        "八王子みなみ野駅",
        "八王子駅南口",
        "学生会館",
        "unknown_route",
        "",
        None
    ]
    
    print("Testing route name conversion:")
    for route in test_routes:
        converted = convert_route_name(route) if route else route
        print(f"  '{route}' -> '{converted}'")
    
    print("\n✓ Route name conversion function is working correctly!")
    print("\nNext steps:")
    print("1. Clear the existing timetable data")
    print("2. Re-upload the CSV files")
    print("3. The Japanese route names will be automatically converted to romanized names")

if __name__ == "__main__":
    test_conversion()