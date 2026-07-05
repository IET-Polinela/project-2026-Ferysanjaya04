#!/bin/bash
# ======================================================
# Script: grant_postgres.sh
# Fungsi: Memberi izin CREATEDB ke user_mhs02, lalu
#         menjalankan backend Django tests
# ======================================================

echo "================================================================"
echo "  Memberi izin CREATEDB ke user_mhs02 untuk testing Django"
echo "================================================================"
echo ""

echo "⚠️  Script ini perlu dijalankan sebagai user POSTGRES SUPERVISOR."
echo "   Di VPS, biasanya jalankan: sudo -u postgres bash $0"
echo ""

# Cek apakah kita bisa akses psql
if ! command -v psql &> /dev/null; then
    echo "❌ psql tidak ditemukan. Install PostgreSQL client terlebih dahulu."
    exit 1
fi

# Cek koneksi sebagai postgres user
echo "🔍 Mencoba koneksi ke PostgreSQL sebagai superuser..."
echo ""

# Jalankan perintah ALTER USER
sudo -u postgres psql -c "ALTER USER user_mhs02 CREATEDB;" 2>/dev/null

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Gagal menjalankan sebagai postgres user."
    echo "   Coba metode alternatif..."
    echo ""
    echo "=== JALANKAN MANUAL via psql ==="
    echo "  1. Masuk ke PostgreSQL:"
    echo "     sudo -u postgres psql"
    echo ""
    echo "  2. Jalankan perintah:"
    echo "     ALTER USER user_mhs02 CREATEDB;"
    echo ""
    echo "  3. Keluar: \\q"
    echo ""
    echo "  4. Lalu jalankan test:"
    echo "     cd ~/project-2026-Ferysanjaya04/server_smartcity"
    echo "     python3 manage.py test main_app --verbosity=2"
    exit 1
fi

echo "✅ Izin CREATEDB berhasil diberikan ke user_mhs02!"
echo ""
echo "================================================================"
echo "  Sekarang menjalankan Django backend tests..."
echo "================================================================"
echo ""

cd "$(dirname "$0")/../server_smartcity" || exit 1

python3 manage.py test main_app --verbosity=2

EXIT_CODE=$?
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ SELURUH TEST BERHASIL! Status: OK"
else
    echo "❌ ADA TEST YANG GAGAL! Status: FAIL"
fi

exit $EXIT_CODE
