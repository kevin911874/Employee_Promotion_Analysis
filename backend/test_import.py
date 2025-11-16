import sys
import os
os.chdir("d:\\Project\\Employee Promotion Analysis\\backend")
sys.path.insert(0, '.')

try:
    print("=" * 50)
    print("Testing app import...")
    print("=" * 50)
    
    print("1. Importing config...")
    from app.config import settings
    print("   ✓ Config OK")
    
    print("2. Importing database...")
    from app.database import connect_to_mongo, close_mongo_connection, get_database
    print("   ✓ Database OK")
    
    print("3. Importing routes...")
    from app.routes import auth, employees, predictions, analytics
    print("   ✓ Routes OK")
    
    print("4. Importing main app...")
    from app.main import app
    print("   ✓ Main app OK")
    
    print("5. App details...")
    print(f"   - Routes count: {len(app.routes)}")
    print(f"   - Middleware count: {len(app.user_middleware)}")
    
    print("=" * 50)
    print("✓ All imports successful!")
    print("=" * 50)
    
except Exception as e:
    import traceback
    print("=" * 50)
    print(f"✗ Error: {e}")
    print("=" * 50)
    traceback.print_exc()
    sys.exit(1)
