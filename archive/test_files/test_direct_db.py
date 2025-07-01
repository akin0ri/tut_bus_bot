#!/usr/bin/env python3
"""Direct database test to check time data"""

import sqlite3
from datetime import datetime

def test_direct_db():
    """Test database directly without Flask app context"""
    
    print("=== Direct Database Time Data Test ===\n")
    
    # Connect to the database
    conn = sqlite3.connect('instance/timetable.db')
    cursor = conn.cursor()
    
    try:
        # Test 1: Check table structure
        print("1. Checking table structure...")
        cursor.execute("PRAGMA table_info(timetable)")
        columns = cursor.fetchall()
        print("   Columns in timetable table:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # Test 2: Get sample data
        print("\n2. Getting sample data...")
        cursor.execute("""
            SELECT id, route, direction, departure_time, arrival_time, 
                   is_shuttle, shuttle_start, shuttle_end, valid_from, valid_to
            FROM timetable 
            LIMIT 10
        """)
        rows = cursor.fetchall()
        
        if not rows:
            print("   ❌ No data found in timetable!")
            return
            
        print(f"   ✓ Found {len(rows)} rows")
        
        # Test 3: Display sample data
        print("\n3. Sample data:")
        for i, row in enumerate(rows[:5]):
            print(f"\n   Row {i+1}:")
            print(f"   - ID: {row[0]}")
            print(f"   - Route: {row[1]}")
            print(f"   - Direction: {row[2]}")
            print(f"   - Departure time: {row[3]} (type: {type(row[3])})")
            print(f"   - Arrival time: {row[4]} (type: {type(row[4])})")
            print(f"   - Is shuttle: {row[5]}")
            print(f"   - Shuttle start: {row[6]}")
            print(f"   - Shuttle end: {row[7]}")
            print(f"   - Valid from: {row[8]}")
            print(f"   - Valid to: {row[9]}")
        
        # Test 4: Check for specific routes
        print("\n4. Checking specific routes...")
        test_routes = ["八王子みなみ野駅", "八王子駅南口", "学生会館", "hachioji", "minamino"]
        for route in test_routes:
            cursor.execute("SELECT COUNT(*) FROM timetable WHERE route = ?", (route,))
            count = cursor.fetchone()[0]
            if count > 0:
                cursor.execute("""
                    SELECT departure_time, arrival_time 
                    FROM timetable 
                    WHERE route = ? 
                    LIMIT 1
                """, (route,))
                sample = cursor.fetchone()
                print(f"   - {route}: {count} entries, sample times: {sample}")
            else:
                print(f"   - {route}: No entries found")
        
        # Test 5: Check for NULL time values
        print("\n5. Checking for NULL or empty time values...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM timetable 
            WHERE departure_time IS NULL OR departure_time = ''
        """)
        null_departure = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM timetable 
            WHERE arrival_time IS NULL OR arrival_time = ''
        """)
        null_arrival = cursor.fetchone()[0]
        
        print(f"   - NULL/empty departure times: {null_departure}")
        print(f"   - NULL/empty arrival times: {null_arrival}")
        
        # Test 6: Check time format
        print("\n6. Checking time formats...")
        cursor.execute("""
            SELECT DISTINCT departure_time 
            FROM timetable 
            WHERE departure_time IS NOT NULL AND departure_time != ''
            LIMIT 10
        """)
        times = cursor.fetchall()
        print("   Sample departure times:")
        for time_val in times:
            print(f"   - {time_val[0]}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    test_direct_db()