# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: citizen_portal.spec.js >> Modul 1: Otorisasi & Sesi (AUTH-04, AUTH-05, AUTH-06) >> AUTH-06: Kedua token kadaluarsa → localStorage dibersihkan, redirect ke #login
- Location: playwright\citizen_portal.spec.js:519:5

# Error details

```
Error: route.continue: New URL must have same protocol as overridden URL
```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - navigation [ref=e2]:
    - link " Smart City Portal" [ref=e4] [cursor=pointer]:
      - /url: "#"
      - generic [ref=e5]: 
      - text: Smart City Portal
  - main [ref=e6]:
    - generic [ref=e8]:
      - generic [ref=e9]:
        - generic [ref=e10]: 
        - heading "Selamat Datang di Smart City Portal" [level=2] [ref=e11]
        - paragraph [ref=e12]: Portal pelaporan warga untuk kota yang lebih baik
        - generic [ref=e13]:
          - link " Login" [ref=e14] [cursor=pointer]:
            - /url: "#login"
            - generic [ref=e15]: 
            - text: Login
          - link " Daftar" [ref=e16] [cursor=pointer]:
            - /url: "#register"
            - generic [ref=e17]: 
            - text: Daftar
      - generic [ref=e19]:
        - heading " Laporan Terbaru Warga" [level=5] [ref=e20]:
          - generic [ref=e21]: 
          - text: Laporan Terbaru Warga
        - generic [ref=e23]:
          - generic [ref=e24]: 
          - paragraph [ref=e25]: Memuat laporan terbaru...
  - text:   
```

# Test source

```ts
  1   | // =============================================================================
  2   | // FILE: citizen_portal.spec.js — E2E Test Suite Playwright
  3   | // =============================================================================
  4   | // DESKRIPSI:
  5   | //   File ini berisi seluruh skenario pengujian End-to-End (E2E) menggunakan
  6   | //   Playwright untuk menguji Portal Citizen dan Portal Admin pada aplikasi Smart City.
  7   | //
  8   | // CARA MENJALANKAN:
  9   | //   1. Pastikan server Django backend aktif:
  10  | //      > cd server_smartcity
  11  | //      > python manage.py runserver
  12  | //
  13  | //   2. Jalankan semua test:
  14  | //      > npx playwright test
  15  | //
  16  | //   3. Untuk mode visual (interaktif):
  17  | //      > npx playwright test --ui
  18  | //
  19  | //   4. Untuk menjalankan test tertentu:
  20  | //      > npx playwright test tests/e2e/citizen_portal.spec.js
  21  | //
  22  | //   5. Untuk mode headed (melihat browser):
  23  | //      > npx playwright test --headed
  24  | //
  25  | // PRASYARAT:
  26  | //   - npm init playwright@latest  (jika belum diinisialisasi)
  27  | //   - Server backend Django harus berjalan di http://localhost:8000
  28  | //   - SPA Citizen Portal harus bisa diakses (via Live Server / file:// / http-server)
  29  | //
  30  | // ARSITEKTUR APLIKASI:
  31  | //   - SPA Citizen Portal: Single Page Application berbasis hash-routing (#login, #register, #dashboard)
  32  | //   - Admin Portal: Server-side rendered Django templates (login, dashboard, report list)
  33  | //   - API Backend: Django REST Framework + SimpleJWT (token-based auth)
  34  | //   - Storage: localStorage menyimpan 'access_token', 'refresh_token', 'username'
  35  | // =============================================================================
  36  | 
  37  | // =========================================================================
  38  | // IMPORT & SETUP
  39  | // ---------------------------------------------------------------------------
  40  | // Mengimpor fungsi 'test' dan 'expect' dari library Playwright.
  41  | // 'test' digunakan untuk mendefinisikan skenario pengujian.
  42  | // 'expect' digunakan untuk melakukan assertion (pemeriksaan hasil).
  43  | //
  44  | // ---------------------------------------------------------------------------
  45  | const { test, expect } = require('@playwright/test');
  46  | const path = require('path');
  47  | const { pathToFileURL } = require('url');
  48  | 
  49  | // =========================================================================
  50  | // MIXED CONTENT FIX - KHUSUS UNTUK IP BACKEND
  51  | // =========================================================================
  52  | // Karena SPA di-host di HTTPS (GitHub Pages) dan API di HTTP,
  53  | // browser memblokir request. Ini adalah fix targeted.
  54  | //
  55  | // Catatan: route harus didaftarkan pada setiap page yang digunakan oleh test,
  56  | // sehingga sebelum tiap navigasi kita pasang interceptor pada page fixture.
  57  | test.beforeEach(async ({ page }) => {
  58  |     await page.route('**/*', async (route) => {
  59  |         const url = route.request().url();
  60  | 
  61  |         if (url.startsWith('http://103.151.63.85:8002/')) {
  62  |             const newUrl = url.replace('http://103.151.63.85:8002', 'https://103.151.63.85:8002');
  63  |             console.log(`[Mixed Content Fix] ${url} → ${newUrl}`);
> 64  |             await route.continue({ url: newUrl });
      |                                 ^ Error: route.continue: New URL must have same protocol as overridden URL
  65  |         } else {
  66  |             await route.continue();
  67  |         }
  68  |     });
  69  | });
  70  | 
  71  | // ---------------------------------------------------------------------------
  72  | // KONSTANTA 
  73  | // ---------------------------------------------------------------------------
  74  | // BASE_URL: Alamat server backend Django. Semua request API diarahkan ke sini.
  75  | //
  76  | // SPA_URL: Alamat di mana SPA Citizen Portal di-serve. Dalam testing,
  77  | //          kita bisa menggunakan file:// protocol atau http-server lokal.
  78  | //          Sesuaikan path ini dengan lokasi file index.html SPA Anda.
  79  | //
  80  | // CATATAN PENTING :
  81  | //   - Jika menggunakan file:// protocol, beberapa fitur (seperti fetch API)
  82  | //     mungkin diblokir oleh kebijakan CORS browser. Disarankan menggunakan
  83  | //     http-server atau Live Server extension.
  84  | // ---------------------------------------------------------------------------
  85  | const BASE_URL = 'http://103.151.63.85:8002';
  86  | 
  87  | // Path ke file SPA relatif terhadap direktori smartcity_citizen_spa_23758041
  88  | // Gunakan file:// protocol untuk akses langsung ke file lokal.
  89  | // CATATAN: fetch API mungkin terblokir oleh CORS di file://,
  90  | // tapi Playwright page.route() akan meng-intercept SEMUA request
  91  | // sebelum mencapai server, sehingga mock API tetap berfungsi.
  92  | const SPA_URL =  'http://192.168.56.1:8080'
  93  | 
  94  | // ---------------------------------------------------------------------------
  95  | // KREDENSIAL TEST 
  96  | // ---------------------------------------------------------------------------
  97  | // Kredensial untuk akun test yang sudah terdaftar di database Django.
  98  | // Pastikan akun ini ada sebelum menjalankan test, atau gunakan mock API.
  99  | // ---------------------------------------------------------------------------
  100 | const TEST_CITIZEN_USERNAME = 'dikin';
  101 | const TEST_CITIZEN_PASSWORD = 'dikin123';
  102 | const TEST_ADMIN_USERNAME  = 'admin1';
  103 | const TEST_ADMIN_PASSWORD  = 'admin123';
  104 | 
  105 | // ---------------------------------------------------------------------------
  106 | // FAKE JWT TOKENS UNTUK TESTING
  107 | // ---------------------------------------------------------------------------
  108 | // Token JWT palsu yang digunakan untuk simulasi sesi kadaluarsa.
  109 | //
  110 | // Struktur JWT: header.payload.signature (base64url encoded)
  111 | //
  112 | // Token di bawah sengaja dibuat dengan 'exp' (expiry) yang sudah lewat
  113 | // sehingga server akan menolaknya dengan status 401 Unauthorized.
  114 | // ---------------------------------------------------------------------------
  115 | const EXPIRED_ACCESS_TOKEN  = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAwMDAwMDAwLCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6ImZha2VfYWNjZXNzX2lkIiwidXNlcl9pZCI6MX0.fake_signature_for_testing';
  116 | const EXPIRED_REFRESH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwMDAwMDAwMCwiaWF0IjoxNjAwMDAwMDAwLCJqdGkiOiJmYWtlX3JlZnJlc2hfaWQiLCJ1c2VyX2lkIjoxfQ.fake_signature_for_testing';
  117 | const VALID_ACCESS_TOKEN    = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo5OTk5OTk5OTk5LCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6InZhbGlkX2FjY2Vzc19pZCIsInVzZXJfaWQiOjF9.fake_valid_signature';
  118 | 
  119 | // =============================================================================
  120 | // CORS HEADERS UNTUK MOCK RESPONSE
  121 | // =============================================================================
  122 | // Karena SPA di-host di GitHub Pages (https://iet-polinela.github.io) dan
  123 | // BASE_URL mengarah ke server produksi (http://103.151.63.85:8002), browser
  124 | // akan mengirim CORS preflight (OPTIONS). Semua mock response HARUS menyertakan
  125 | // header CORS agar browser tidak memblokir response.
  126 | // =============================================================================
  127 | const CORS_HEADERS = {
  128 |     'Access-Control-Allow-Origin': '*',
  129 |     'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH',
  130 |     'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  131 | };
  132 | 
  133 | // =============================================================================
  134 | // FUNGSI HELPER 
  135 | // =============================================================================
  136 | // Fungsi-fungsi pembantu (helper) yang digunakan berulang kali di berbagai test.
  137 | // Memisahkan logika ke helper function membuat kode test lebih bersih dan DRY
  138 | // (Don't Repeat Yourself).
  139 | //
  140 | // =============================================================================
  141 | 
  142 | /**
  143 |  * loginSPA - Melakukan login ke Portal Warga (Citizen SPA)
  144 |  *
  145 |  * Langkah-langkah / Steps:
  146 |  *   1. Navigasi ke halaman SPA dengan hash #login
  147 |  *   2. Tunggu form login muncul (id='loginForm')
  148 |  *   3. Isi username dan password
  149 |  *   4. Klik tombol submit
  150 |  *   5. Tunggu navigasi ke #dashboard (jika login berhasil)
  151 |  *
  152 |  * @param {import('@playwright/test').Page} page - Objek halaman Playwright 
  153 |  * @param {string} username - Username untuk login 
  154 |  * @param {string} password - Password untuk login 
  155 |  */
  156 | async function loginSPA(page, username, password) {
  157 |     // Navigasi ke halaman login SPA
  158 |     await page.goto(`${SPA_URL}#login`);
  159 | 
  160 |     // Tunggu hingga form login ter-render di DOM
  161 |     // Catatan: SPA menggunakan hash-routing, jadi router.js akan meng-inject
  162 |     //          HTML form login ke dalam div #app-content saat hash = #login
  163 |     await page.waitForSelector('#loginForm', { state: 'visible', timeout: 10000 });
  164 | 
```