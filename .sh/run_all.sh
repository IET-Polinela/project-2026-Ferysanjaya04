#!/bin/bash
# ======================================================
# Script: run_all.sh
# Fungsi: Menjalankan seluruh rangkaian testing secara
#         otomatis tanpa interaksi manual:
#   1. Backend Django Tests
#   2. Frontend Playwright Tests (headless)
#   3. Code Coverage Measurement
#
# Usage:
#   bash run_all.sh              # full suite (tanpa HTML coverage)
#   bash run_all.sh --html       # full suite + HTML coverage report
#   bash run_all.sh --backend    # hanya backend test
#   bash run_all.sh --frontend   # hanya frontend test
#   bash run_all.sh --coverage   # hanya coverage
# ======================================================

SCRIPT_DIR="$(dirname "$0")"
START_TIME=$(date +%s)
MODE="${1:-all}"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     SMART CITY - COMPREHENSIVE TEST SUITE    ║"
echo "╠══════════════════════════════════════════════╣"
echo "║  1. Backend Django REST API Tests            ║"
echo "║  2. Frontend E2E Playwright Tests            ║"
echo "║  3. Code Coverage Measurement                ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Fungsi untuk menjalankan backend test
run_backend() {
    echo ""
    echo "═══════════════════════════════════════════════"
    echo "  STEP 1/3: Backend Django REST API Tests"
    echo "═══════════════════════════════════════════════"
    echo ""
    bash "$SCRIPT_DIR/test_backend.sh"
    return $?
}

# Fungsi untuk menjalankan frontend test
run_frontend() {
    echo ""
    echo "═══════════════════════════════════════════════"
    echo "  STEP 2/3: Frontend E2E Playwright Tests"
    echo "═══════════════════════════════════════════════"
    echo ""
    bash "$SCRIPT_DIR/test_frontend.sh" "headless"
    return $?
}

# Fungsi untuk menjalankan coverage
run_coverage() {
    echo ""
    echo "═══════════════════════════════════════════════"
    echo "  STEP 3/3: Code Coverage Measurement"
    echo "═══════════════════════════════════════════════"
    echo ""
    if [ "$GENERATE_HTML" = true ]; then
        bash "$SCRIPT_DIR/coverage.sh" "html"
    else
        bash "$SCRIPT_DIR/coverage.sh"
    fi
    return $?
}

BACKEND_EXIT=0
FRONTEND_EXIT=0
COVERAGE_EXIT=0
GENERATE_HTML=false

# Parse arguments
if [ "$MODE" = "--html" ]; then
    GENERATE_HTML=true
    MODE="all"
elif [ "$2" = "--html" ]; then
    GENERATE_HTML=true
fi

case "$MODE" in
    "backend")
        run_backend
        BACKEND_EXIT=$?
        ;;
    "frontend")
        run_frontend
        FRONTEND_EXIT=$?
        ;;
    "coverage")
        run_coverage
        COVERAGE_EXIT=$?
        ;;
    "all")
        # Step 1: Backend
        run_backend
        BACKEND_EXIT=$?
        if [ $BACKEND_EXIT -ne 0 ]; then
            echo ""
            echo "❌ BACKEND TEST GAGAL! Hentikan eksekusi."
            echo "   Perbaiki error sebelum melanjutkan."
            exit $BACKEND_EXIT
        fi

        # Step 2: Frontend
        run_frontend
        FRONTEND_EXIT=$?
        if [ $FRONTEND_EXIT -ne 0 ]; then
            echo ""
            echo "❌ FRONTEND TEST GAGAL! Hentikan eksekusi."
            echo "   Perbaiki error sebelum melanjutkan."
            exit $FRONTEND_EXIT
        fi

        # Step 3: Coverage
        run_coverage
        COVERAGE_EXIT=$?
        ;;
    *)
        echo "❌ Argumen tidak dikenal: $MODE"
        echo "   Gunakan: bash run_all.sh [backend|frontend|coverage|all|--html]"
        exit 1
        ;;
esac

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║         TEST SUITE SELESAI!                  ║"
echo "╠══════════════════════════════════════════════╣"
printf "║  Backend Tests    : %s                      ║\n" "$([ $BACKEND_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
printf "║  Frontend Tests   : %s                      ║\n" "$([ $FRONTEND_EXIT -eq 0 ] && echo '✅ PASS' || echo '❌ FAIL')"
printf "║  Code Coverage    : %s                      ║\n" "$([ $COVERAGE_EXIT -eq 0 ] && echo '✅ DONE' || echo '⚠️  SKIP')"
printf "║  Total Duration   : %ds                      ║\n" "$DURATION"
echo "╚══════════════════════════════════════════════╝"

if [ $BACKEND_EXIT -eq 0 ] && [ $FRONTEND_EXIT -eq 0 ]; then
    echo ""
    echo "🎉 SEMUA TEST BERHASIL! Status: OK"
else
    echo ""
    echo "⚠️  Masih ada test yang gagal. Analisis traceback error di atas."
fi

exit $((BACKEND_EXIT | FRONTEND_EXIT | COVERAGE_EXIT))
