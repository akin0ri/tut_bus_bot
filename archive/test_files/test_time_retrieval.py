#!/usr/bin/env python3
"""Test script to diagnose time data retrieval issues"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.timetable import Timetable
from datetime import datetime, time

def test_time_retrieval():
    """Test time data storage and retrieval"""
    app = create_app()
    
    with app.app_context():
        print("=== Time Data Retrieval Test ===\n")
        
        # Test 1: Check database content
        print("1. Checking database content...")
        timetables = Timetable.query.limit(10).all()
        
        if not timetables:
            print("   ❌ No timetables found in database!")
            return
            
        print(f"   ✓ Found {len(timetables)} timetables")
        
        # Test 2: Check time field types and values
        print("\n2. Checking time field types and values...")
        for i, t in enumerate(timetables[:5]):
            print(f"\n   Timetable {i+1}:")
            print(f"   - Route: {t.route}")
            print(f"   - Direction: {t.direction}")
            print(f"   - Departure time type: {type(t.departure_time)}")
            print(f"   - Departure time value: {t.departure_time}")
            print(f"   - Arrival time type: {type(t.arrival_time)}")
            print(f"   - Arrival time value: {t.arrival_time}")
            
            # Test formatting
            if t.departure_time:
                try:
                    formatted = t.departure_time.strftime('%H:%M:%S')
                    print(f"   - Formatted departure: {formatted}")
                except Exception as e:
                    print(f"   - ❌ Error formatting departure time: {e}")
                    
            if t.arrival_time:
                try:
                    formatted = t.arrival_time.strftime('%H:%M:%S')
                    print(f"   - Formatted arrival: {formatted}")
                except Exception as e:
                    print(f"   - ❌ Error formatting arrival time: {e}")
        
        # Test 3: Query with time filtering
        print("\n3. Testing time filtering...")
        test_time = time(10, 0, 0)  # 10:00:00
        filtered = Timetable.query.filter(Timetable.departure_time > test_time).limit(5).all()
        print(f"   Found {len(filtered)} timetables with departure after 10:00:00")
        
        # Test 4: Check for NULL values
        print("\n4. Checking for NULL time values...")
        null_departure = Timetable.query.filter(Timetable.departure_time == None).count()
        null_arrival = Timetable.query.filter(Timetable.arrival_time == None).count()
        print(f"   - NULL departure times: {null_departure}")
        print(f"   - NULL arrival times: {null_arrival}")
        
        # Test 5: Raw SQL query to check actual database values
        print("\n5. Checking raw database values...")
        result = db.session.execute(
            db.text("SELECT id, route, departure_time, arrival_time FROM timetable LIMIT 5")
        )
        for row in result:
            print(f"   ID {row[0]}: departure={row[2]}, arrival={row[3]}")
        
        # Test 6: Test specific route time retrieval
        print("\n6. Testing specific route retrieval...")
        test_routes = ["八王子みなみ野駅", "八王子駅南口", "学生会館"]
        for route in test_routes:
            count = Timetable.query.filter(Timetable.route == route).count()
            if count > 0:
                first = Timetable.query.filter(Timetable.route == route).first()
                print(f"   - {route}: {count} entries, first departure: {first.departure_time}")
            else:
                print(f"   - {route}: No entries found")

if __name__ == "__main__":
    test_time_retrieval()