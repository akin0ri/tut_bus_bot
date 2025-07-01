# Time Data Retrieval Issue - Investigation Summary

## Issues Found

### 1. **Route Name Mismatch (PRIMARY ISSUE)**
- **Problem**: CSV files use Japanese route names, but the database expects romanized names
- **CSV route names**: 
  - "八王子みなみ野駅" 
  - "八王子駅南口"
  - "学生会館"
- **Expected database names**:
  - "minamino"
  - "hachioji" 
  - "dormitory"
- **Impact**: Data is uploaded but cannot be retrieved because queries use romanized names while data is stored with Japanese names

### 2. **Missing timetable_type Column**
- **Problem**: CSV files don't include `timetable_type` column
- **Current handling**: Defaults to 1 (weekday) in upload code
- **CSV filenames suggest type**:
  - schoolbus_weekday.csv → timetable_type = 1
  - schoolbus_saturday.csv → timetable_type = 2
  - schoolbus_holiday.csv → timetable_type = 3

### 3. **Time Format**
- **Current state**: Times are stored correctly as TIME type with microseconds (e.g., "07:15:00.000000")
- **No issue here**: SQLAlchemy handles the conversion properly

## Solution Implemented

### Route Name Mapping
Added a conversion function to three files:
1. `app/blueprints/admin/routes.py` - Admin upload route
2. `app/blueprints/api/routes.py` - API upload route  
3. `app/utils/csv_utils.py` - CSV utility functions

```python
ROUTE_NAME_MAPPING = {
    "八王子みなみ野駅": "minamino",
    "八王子駅南口": "hachioji", 
    "学生会館": "dormitory"
}

def convert_route_name(japanese_name):
    """Convert Japanese route name to romanized version"""
    return ROUTE_NAME_MAPPING.get(japanese_name, japanese_name)
```

### Usage in Upload Code
Changed from:
```python
route = str(row['route']) if not pd.isna(row['route']) else ''
```

To:
```python
route_raw = str(row['route']) if not pd.isna(row['route']) else ''
route = convert_route_name(route_raw)
```

## Next Steps

1. **Clear existing data**: Delete all timetable entries that have Japanese route names
2. **Re-upload CSV files**: The conversion will automatically apply
3. **Verify data**: Check that routes are stored as "hachioji", "minamino", "dormitory"
4. **Test retrieval**: Confirm that time data can be retrieved correctly

## Additional Recommendations

1. **Add timetable_type to CSV**: Consider adding this column to CSV files for clarity
2. **Validation**: Add validation to ensure route names are in the expected format
3. **Error handling**: Add specific error messages when invalid route names are encountered
4. **Documentation**: Document the expected route name format for future uploads