from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILES_DIRS = [
     BASE_DIR / "static",
 ]