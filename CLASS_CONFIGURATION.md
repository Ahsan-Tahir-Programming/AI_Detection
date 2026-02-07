# Class Configuration Management

## Overview
Moved hardcoded class names and colors from Python code to a centralized `classes.txt` file in the assets folder for easy maintenance and updates.

## File Structure

### `app/assets/classes.txt`
Centralized configuration file containing all class definitions with mappings and colors.

**Format:**
```
YOLO_CLASS_NAME|MAPPED_CLASS_NAME|RGB_R|RGB_G|RGB_B
```

**Example:**
```
Backlit Not Functional|backlit_not_functional|255|0|0
Backlit Functional|backlit_functional|0|255|0
BWU Damage|sheet_damaged|255|165|0
```

**Fields:**
- `YOLO_CLASS_NAME`: Original class name from YOLO model detection
- `MAPPED_CLASS_NAME`: Internal mapped name used in database and API responses
- `RGB_R`: Red color component (0-255)
- `RGB_G`: Green color component (0-255)
- `RGB_B`: Blue color component (0-255)

## How It Works

### Updated: `app/core/config.py`

Now dynamically loads classes from `classes.txt` at startup:

```python
# Load class names, colors, and mappings from classes.txt file
CLASSES_FILE = os.path.join(APP_DIR, "assets", "classes.txt")

CLASS_COLORS = {}
CLASS_NAME_MAP = {}

if os.path.exists(CLASSES_FILE):
    with open(CLASSES_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('|')
            if len(parts) >= 4:
                yolo_class = parts[0]
                mapped_class = parts[1]
                try:
                    r, g, b = int(parts[2]), int(parts[3]), int(parts[4])
                    CLASS_COLORS[yolo_class] = (r, g, b)
                    CLASS_NAME_MAP[yolo_class] = mapped_class
                except (ValueError, IndexError):
                    print(f"Warning: Could not parse class line: {line}")
else:
    # Fallback to hardcoded values if file doesn't exist
    ...
```

**Key Features:**
- ✅ Dynamic loading from `classes.txt`
- ✅ Comment support (lines starting with `#`)
- ✅ Error handling for malformed lines
- ✅ Fallback to hardcoded values if file is missing
- ✅ Clear warning messages on startup

## Usage in Code

No code changes needed! All existing imports work the same:

```python
from app.core.config import CLASS_COLORS, CLASS_NAME_MAP

# Use exactly as before
color = CLASS_COLORS.get("Backlit Not Functional")  # Returns (255, 0, 0)
mapped = CLASS_NAME_MAP.get("Backlit Not Functional")  # Returns "backlit_not_functional"
```

## Adding New Classes

To add a new detection class:

1. **Edit** `app/assets/classes.txt`
2. **Add a line** with the format:
   ```
   NEW_CLASS_NAME|new_class_name|R|G|B
   ```
3. **Restart** the backend server

Example - adding a new class:
```
Paint Damage|paint_damage|200|100|50
```

## Benefits

✅ **Easy Maintenance**: Edit classes without touching Python code
✅ **No Redeploy**: Update classes.txt in production environment
✅ **Version Control**: Easier to track class changes in git
✅ **Flexibility**: Add/remove classes dynamically
✅ **Better Organization**: Separates configuration from logic
✅ **Fallback Support**: Works even if file is missing

## Backward Compatibility

✅ **No Breaking Changes**: If `classes.txt` is missing, the system falls back to hardcoded values and prints a warning

## File Locations

```
app/
├── assets/
│   ├── ARIALBD.TTF          (font file)
│   └── classes.txt          (NEW: class configuration)
├── core/
│   ├── config.py            (UPDATED: loads from classes.txt)
│   ├── logger.py
│   └── __init__.py
└── ...
```

## Deployment Notes

### Docker Deployment
The `classes.txt` file will be available in Docker containers at:
```
/app/assets/classes.txt
```

### Local Development
File location:
```
app/assets/classes.txt
```

## Testing

Verify classes load correctly:

```bash
cd c:/ahsan/ahsan-work/personnel\ github\ projects/python/Ai_Detection
python -c "from app.core.config import CLASS_COLORS, CLASS_NAME_MAP; print(f'Loaded {len(CLASS_COLORS)} classes')"
```

Output should be:
```
Loaded 9 classes
```

## Future Enhancements

1. **JSON Format**: Convert to `classes.json` for more structure
   ```json
   {
     "classes": [
       {
         "yolo_name": "Backlit Not Functional",
         "mapped_name": "backlit_not_functional",
         "color": [255, 0, 0]
       }
     ]
   }
   ```

2. **YAML Support**: Use `classes.yaml` for readability
   ```yaml
   Backlit Not Functional:
     mapped_name: backlit_not_functional
     color: [255, 0, 0]
   ```

3. **Database Integration**: Store class definitions in SQLite for dynamic updates

4. **API Endpoint**: Expose available classes via `/api/classes` endpoint
   ```python
   @router.get('/classes/')
   async def get_classes():
       """Get all available detection classes"""
       return CLASS_NAME_MAP
   ```
