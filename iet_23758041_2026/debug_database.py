#!/usr/bin/env python
import os
import sys
import django

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iet_23758041_2026.settings')
django.setup()

from main_app.models import Report
from django.db import connection

print("=" * 70)
print("DATABASE CONFIGURATION CHECK")
print("=" * 70)

# Cek konfigurasi database
from django.conf import settings
db_config = settings.DATABASES['default']
print(f"\nEngine: {db_config['ENGINE']}")
print(f"Database Name: {db_config['NAME']}")
print(f"Host: {db_config['HOST']}")
print(f"Port: {db_config['PORT']}")
print(f"User: {db_config['USER']}")

print("\n" + "=" * 70)
print("DATA CHECK")
print("=" * 70)

# Cek koneksi
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("\n✓ Database connection: SUCCESS")
except Exception as e:
    print(f"\n✗ Database connection ERROR: {e}")
    sys.exit(1)

# Cek data Report
print(f"\nTotal Reports in Database: {Report.objects.count()}")

reports = Report.objects.all()
if reports.exists():
    print("\nReport Details:")
    for i, report in enumerate(reports, 1):
        print(f"\n--- Report #{i} ---")
        print(f"ID: {report.id}")
        print(f"Title: {report.title}")
        print(f"Category: {report.category} ({report.get_category_display()})")
        print(f"Location: {report.location}")
        print(f"Status: {report.status} ({report.get_status_display()})")
        print(f"Description: {report.description[:100]}...")
        print(f"Created: {report.created_at}")
        print(f"Updated: {report.updated_at}")
else:
    print("\n✗ NO DATA FOUND in main_app_report table!")
    
# Cek tabel yang ada
print("\n" + "=" * 70)
print("CHECKING TABLES IN DATABASE")
print("=" * 70)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    print(f"\nTables in database: {len(tables) if tables else 0}")
    for table in tables:
        print(f"  - {table[0]}")
        
    # Check if main_app_report exists
    if any('main_app_report' in table[0] for table in tables):
        print("\n✓ main_app_report table EXISTS")
        # Cek jumlah records
        cursor.execute("SELECT COUNT(*) FROM main_app_report;")
        count = cursor.fetchone()[0]
        print(f"Records in main_app_report: {count}")
    else:
        print("\n✗ main_app_report table NOT FOUND!")

print("\n" + "=" * 70)
