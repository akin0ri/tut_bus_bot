#!/usr/bin/env python3
"""Test route name mapping issue"""

import sqlite3

def test_route_mapping():
    """Test route name mapping between CSV and database"""
    
    print("=== Route Name Mapping Test ===\n")
    
    # Connect to the database
    conn = sqlite3.connect('instance/timetable.db')
    cursor = conn.cursor()
    
    try:
        # Get all unique route names
        print("1. Unique route names in database:")
        cursor.execute("SELECT DISTINCT route FROM timetable")
        routes = cursor.fetchall()
        for route in routes:
            print(f"   - {route[0]}")
        
        # Check if there are any Japanese route names
        print("\n2. Checking for Japanese route names...")
        japanese_routes = ["八王子みなみ野駅", "八王子駅南口", "学生会館"]
        for jp_route in japanese_routes:
            cursor.execute("SELECT COUNT(*) FROM timetable WHERE route = ?", (jp_route,))
            count = cursor.fetchone()[0]
            print(f"   - {jp_route}: {count} entries")
        
        # Proposed mapping
        print("\n3. Proposed route name mapping:")
        route_mapping = {
            "八王子みなみ野駅": "minamino",
            "八王子駅南口": "hachioji",
            "学生会館": "dormitory"
        }
        
        for jp_name, en_name in route_mapping.items():
            cursor.execute("SELECT COUNT(*) FROM timetable WHERE route = ?", (en_name,))
            count = cursor.fetchone()[0]
            print(f"   - {jp_name} -> {en_name}: {count} entries in DB")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    test_route_mapping()