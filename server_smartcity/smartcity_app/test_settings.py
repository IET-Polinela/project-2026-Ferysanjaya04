"""
Test settings untuk Smart City.
Menggunakan SQLite agar testing bisa berjalan tanpa izin CREATEDB di PostgreSQL.
Cara pakai: python manage.py test main_app --settings=smartcity_app.test_settings
"""

from .settings import *  # noqa: F401,F403

# ==============================================================================
# OVERRIDE DATABASE — Gunakan SQLite untuk testing
# ==============================================================================
# Alasan: User PostgreSQL (user_mhs02) tidak memiliki izin CREATEDB,
# sehingga Django tidak bisa membuat database test (test_db_mhs02).
# SQLite tidak memerlukan izin khusus dan tetap berfungsi penuh untuk testing.
#
# Catatan: Perubahan ini HANYA berlaku saat menjalankan test menggunakan
# --settings=smartcity_app.test_settings. Database production (PostgreSQL)
# tetap aman dan tidak terpengaruh.
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}
