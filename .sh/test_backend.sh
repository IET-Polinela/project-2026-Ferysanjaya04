#!/bin/bash
# ======================================================
# Script: test_backend.sh
# Fungsi: Menjalankan pengujian Backend Django REST API
# ======================================================

SETTINGS="${1:-smartcity_app.test_settings}"  # default: test_settings (SQLite)

echo "=============================================="
echo "  Running Backend Django REST API Tests"
echo "=============================================="
echo "  Settings: $SETTINGS"
echo "=============================================="

# Masuk ke direktori server_smartcity
cd "$(dirname "$0")/../server_smartcity" || { echo "❌ Gagal masuk ke direktori server_smartcity"; exit 1; }

# Aktifkan virtual environment jika ada
if [ -d "../venv" ]; then
    echo "📦 Mengaktifkan virtual environment (../venv)..."
    source ../venv/bin/activate 2>/dev/null || source ../venv/Scripts/activate 2>/dev/null
elif [ -d "venv" ]; then
    echo "📦 Mengaktifkan virtual environment (venv)..."
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

echo ""
echo "📋 Menjalankan: python manage.py test main_app --settings=$SETTINGS --verbosity=2"
echo ""

# Jalankan test dengan manage.py (pakai test_settings agar pakai SQLite)
python manage.py test main_app --settings="$SETTINGS" --verbosity=2

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ SELURUH TEST BACKEND BERHASIL! Status: OK"
else
    echo "❌ ADA TEST BACKEND YANG GAGAL! Status: FAIL"
    echo "   Analisis error traceback di atas, lalu perbaiki kode di views/models."
fi

exit $EXIT_CODE
