from pathlib import Path
import sys


SERVICE_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = SERVICE_ROOT / "app"

if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))
