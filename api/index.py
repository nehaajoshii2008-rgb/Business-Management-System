import os
import sys
import shutil

# Ensure base directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Copy db.sqlite3 to writable /tmp directory if running on Vercel
if os.environ.get('VERCEL') or os.environ.get('NOW_REGION'):
    tmp_db = '/tmp/db.sqlite3'
    orig_db = os.path.join(BASE_DIR, 'db.sqlite3')
    if not os.path.exists(tmp_db) and os.path.exists(orig_db):
        try:
            shutil.copy2(orig_db, tmp_db)
        except Exception:
            pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isbms.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application
