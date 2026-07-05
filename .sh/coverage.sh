#!/bin/bash
# ======================================================
# Script: coverage.sh
# Fungsi: Mengukur Code Coverage Backend Django
# ======================================================

HTML_REPORT="${1:-}"  # isi "html" untuk generate HTML report
SETTINGS="${2:-smartcity_app.test_settings}"  # default: test_settings (SQLite)

echo "=============================================="
echo "  Code Coverage Measurement - Backend"
echo "  Settings: $SETTINGS"
echo "=============================================="

SCRIPT_DIR="$(dirname "$0")"
cd "$SCRIPT_DIR/../server_smartcity" || { echo "❌ Gagal masuk direktori server_smartcity"; exit 1; }

# Aktifkan virtual environment jika ada
if [ -d "../venv" ]; then
    source ../venv/bin/activate 2>/dev/null || source ../venv/Scripts/activate 2>/dev/null
elif [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

# ---------------------------
# 1. Install coverage jika belum ada
# ---------------------------
echo ""
echo "📦 Memastikan package coverage terinstall..."
pip install coverage -q

# ---------------------------
# 2. Jalankan test dengan coverage tracking
# ---------------------------
echo ""
echo "📊 Menjalankan: coverage run manage.py test main_app --settings=$SETTINGS --verbosity=2"
echo ""

coverage run manage.py test main_app --settings="$SETTINGS" --verbosity=2

TEST_EXIT=$?
if [ $TEST_EXIT -ne 0 ]; then
    echo ""
    echo "❌ ADA TEST YANG GAGAL! Coverage tidak dapat diukur."
    echo "   Perbaiki test terlebih dahulu sebelum mengukur coverage."
    exit $TEST_EXIT
fi

# ---------------------------
# 3. Generate coverage report
# ---------------------------
echo ""
echo "=============================================="
echo "  📋 Coverage Report Summary"
echo "=============================================="
echo ""

coverage report

# Ambil persentase total coverage dari baris terakhir (kolom terakhir = total)
COVERAGE_LINE=$(coverage report | grep "^TOTAL")
if [ -z "$COVERAGE_LINE" ]; then
    # Fallback: ambil dari baris terakhir
    COVERAGE_PCT=$(coverage report | tail -1 | awk '{print $NF}' | tr -d '%')
else
    COVERAGE_PCT=$(echo "$COVERAGE_LINE" | awk '{print $NF}' | tr -d '%')
fi

echo ""
echo "=============================================="
echo "  📊 Total Code Coverage: ${COVERAGE_PCT}%"
echo "=============================================="

# Validasi minimal 80%
if [ "$COVERAGE_PCT" -ge 80 ] 2>/dev/null; then
    echo "  ✅ Code Coverage (${COVERAGE_PCT}%) >= 80% — MEMENUHI SYARAT"
else
    echo "  ⚠️  Code Coverage (${COVERAGE_PCT}%) < 80% — BELUM MEMENUHI SYARAT"
    echo "     Tambahkan test script untuk meningkatkan cakupan coverage."
fi

# ---------------------------
# 4. Generate HTML report (opsional)
# ---------------------------
if [ "$HTML_REPORT" = "html" ]; then
    echo ""
    echo "📁 Membuat HTML coverage report..."
    python -m coverage html
    echo "   Report tersedia di: server_smartcity/htmlcov/index.html"
fi

echo ""
echo "✅ Coverage measurement selesai!"
exit 0
