#!/bin/bash
# ======================================================
# Script: test_frontend.sh
# Fungsi: Menjalankan pengujian Frontend E2E Playwright
# untuk Portal Citizen SPA
# ======================================================

MODE="${1:-headless}"  # default: headless; gunakan "headed" untuk GUI

echo "=============================================="
echo "  Running Frontend E2E Playwright Tests"
echo "  Mode: $MODE"
echo "=============================================="

SCRIPT_DIR="$(dirname "$0")"
PROJECT_DIR="$SCRIPT_DIR/.."
FRONTEND_DIR="$PROJECT_DIR/smartcity_citizen_spa_23758041"
BACKEND_DIR="$PROJECT_DIR/server_smartcity"

# Trap untuk cleanup jika script dihentikan
cleanup() {
    echo ""
    echo "🧹 Membersihkan proses background..."
    kill $BACKEND_PID 2>/dev/null
    wait $BACKEND_PID 2>/dev/null
    echo "   Selesai."
}
trap cleanup EXIT INT TERM

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Direktori frontend tidak ditemukan: $FRONTEND_DIR"
    exit 1
fi

cd "$FRONTEND_DIR" || exit 1

# ---------------------------
# 1. Inisialisasi npm jika belum ada
# ---------------------------
if [ ! -f "package.json" ]; then
    echo ""
    echo "📦 Inisialisasi npm package manager..."
    npm init -y
fi

# ---------------------------
# 2. Install dependencies (jika node_modules belum ada)
# ---------------------------
if [ ! -d "node_modules" ]; then
    echo ""
    echo "📥 Menginstall npm dependencies..."
    npm install
fi

# ---------------------------
# 3. Download browser Chromium jika belum ada
# ---------------------------
echo ""
echo "🌐 Memastikan Chromium browser untuk Playwright tersedia..."
if [ ! -d "$HOME/.cache/ms-playwright" ] && [ ! -d "%USERPROFILE%\\AppData\\Local\\ms-playwright" ]; then
    npx playwright install chromium
else
    echo "   ✅ Chromium sudah tersedia."
fi

# ---------------------------
# 4. Jalankan backend Django server
# ---------------------------
echo ""
echo "🚀 Menjalankan backend Django server..."
cd "$BACKEND_DIR" || exit 1

# Aktifkan virtual environment
if [ -d "../venv" ]; then
    source ../venv/bin/activate 2>/dev/null || source ../venv/Scripts/activate 2>/dev/null
elif [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

# Cek apakah port 8000 sudah dipakai
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "   ⚠️  Port 8000 sudah dipakai. Menggunakan server yang sudah berjalan."
    BACKEND_PID=""
else
    echo "   Memulai Django server di background..."
    python manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!

    # Tunggu server siap (max 15 detik)
    for i in $(seq 1 15); do
        if curl -s http://localhost:8000/ > /dev/null 2>&1; then
            echo "   ✅ Backend server siap di http://localhost:8000"
            break
        fi
        if [ $i -eq 15 ]; then
            echo "❌ Gagal menjalankan backend server."
            exit 1
        fi
        sleep 1
    done
fi

cd "$FRONTEND_DIR" || exit 1

# ---------------------------
# 5. Jalankan Playwright test
# ---------------------------
echo ""
echo "🎭 Menjalankan Playwright test..."
echo ""

if [ "$MODE" = "headed" ]; then
    npx playwright test --headed
else
    npx playwright test
fi

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ SELURUH PLAYWRIGHT TEST BERHASIL!"
else
    echo "❌ ADA PLAYWRIGHT TEST YANG GAGAL!"
    echo "   Periksa detail error di atas."
fi

exit $EXIT_CODE
