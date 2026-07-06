# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: citizen_portal.spec.js >> Modul 1: Otorisasi & Sesi (AUTH-04, AUTH-05, AUTH-06) >> AUTH-04: Akses #dashboard tanpa token → redirect ke #login
- Location: playwright\citizen_portal.spec.js:359:5

# Error details

```
Error: route.continue: New URL must have same protocol as overridden URL
```

```
Error: page.goto: Test ended.
Call log:
  - navigating to "http://192.168.56.1:8080/", waiting until "load"

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
  230 |             localStorage.setItem('refresh_token', refresh);
  231 |             localStorage.setItem('username', user);
  232 |         },
  233 |         // Argumen kedua: objek data yang di-pass ke browser context
  234 |         { access: accessToken, refresh: refreshToken, user: username }
  235 |     );
  236 | }
  237 | 
  238 | /**
  239 |  * clearAuthTokens - Menghapus semua token dari localStorage
  240 |  *
  241 |  * Digunakan di beforeEach untuk memastikan setiap test dimulai
  242 |  * dari state bersih (tidak ada sesi login tersisa).
  243 |  *
  244 |  * @param {import('@playwright/test').Page} page - Objek halaman Playwright 
  245 |  */
  246 | async function clearAuthTokens(page) {
  247 |     await page.evaluate(() => {
  248 |         // localStorage.clear() menghapus SEMUA data di localStorage domain ini
  249 |         localStorage.clear();
  250 |     });
  251 | }
  252 | 
  253 | /**
  254 |  * mockSPAApiUrl - Memastikan SEMUA request API di SPA mengarah ke localhost:8000
  255 |  *
  256 |  * Menggunakan wildcard untuk path API, fungsi ini akan mencegat request ke domain apapun
  257 |  * (misal: http://103.151.63.71:8013/api, http://192.168.1.5/api, dll)
  258 |  * dan membelokkannya secara paksa ke server Django lokal di http://localhost:8000/api.
  259 |  *
  260 |  * @param {import('@playwright/test').Page} page - Objek halaman Playwright
  261 |  */
  262 | async function mockSPAApiUrl(page) {
  263 |     const BASE_URL = 'http://localhost:8000';
  264 | 
  265 |     // Gunakan wildcard **/api/** untuk menangkap dari host/domain mana saja
  266 |     await page.route('**/api/**', async (route) => {
  267 |         const originalUrl = route.request().url();
  268 | 
  269 |         // [PENTING] Mencegah infinite loop: 
  270 |         // Jika request sudah benar mengarah ke localhost:8000, biarkan saja lewat.
  271 |         if (originalUrl.startsWith(BASE_URL)) {
  272 |             return route.fallback();
  273 |         }
  274 | 
  275 |         // Parsing URL asli menggunakan objek URL bawaan JavaScript
  276 |         const urlObj = new URL(originalUrl);
  277 |         
  278 |         // urlObj.pathname akan mengambil "/api/endpoint/"
  279 |         // urlObj.search akan mengambil query string (misal: "?search=jalan") jika ada
  280 |         const newUrl = `${BASE_URL}${urlObj.pathname}${urlObj.search}`;
  281 | 
  282 |         // Gunakan route.fallback() agar handler route lain (misal mock 401) 
  283 |         // bisa menangani request ini TERLEBIH DAHULU sebelum request dikirim ke server.
  284 |         // Berbeda dengan route.continue(), route.fallback() memberikan kesempatan
  285 |         // ke handler route yang terdaftar setelahnya untuk memproses request.
  286 |         await route.fallback({ url: newUrl });
  287 |     });
  288 | }
  289 | 
  290 | 
  291 | // #############################################################################
  292 | // #                                                                           #
  293 | // #   MODUL 1: OTORISASI & SESI (AUTH-04, AUTH-05, AUTH-06)                   #
  294 | // #                                                                           #
  295 | // #   Modul ini menguji mekanisme perlindungan rute (auth guard) pada SPA.    #
  296 | // #                                                                           #
  297 | // #   Konsep yang diuji:                                                      #
  298 | // #   - Auth Guard: redirect pengguna yang belum login ke halaman login       #
  299 | // #   - Token Expiry: penanganan token JWT yang sudah kadaluarsa              #
  300 | // #   - Session Cleanup: pembersihan localStorage saat sesi berakhir          #
  301 | // #                                                                           #
  302 | // #############################################################################
  303 | 
  304 | test.describe('Modul 1: Otorisasi & Sesi (AUTH-04, AUTH-05, AUTH-06)', () => {
  305 |     // =========================================================================
  306 |     // PENGANTAR MODUL
  307 |     // =========================================================================
  308 |     // Setiap aplikasi SPA yang menggunakan token-based authentication (JWT)
  309 |     // harus memiliki mekanisme auth guard yang melindungi halaman tertentu
  310 |     // dari akses tanpa otentikasi.
  311 |     //
  312 |     // Dalam aplikasi ini (lihat router.js baris 122-139):
  313 |     //   - Fungsi handleRouting() memeriksa token di localStorage
  314 |     //   - Jika TIDAK ada token dan user mengakses #dashboard → redirect ke #login
  315 |     //   - Jika ADA token dan user mengakses #login/#register → redirect ke #dashboard
  316 |     // =========================================================================
  317 | 
  318 |     // -------------------------------------------------------------------------
  319 |     // beforeEach: Dijalankan sebelum SETIAP test dalam describe block ini.
  320 |     //
  321 |     // Tujuan: Membersihkan state browser agar setiap test independen.
  322 |     //
  323 |     // PRINSIP TESTING:
  324 |     //   Setiap test harus bisa berjalan secara independen (isolated).
  325 |     //   Hasil test A tidak boleh mempengaruhi test B.
  326 |     // -------------------------------------------------------------------------
  327 |     test.beforeEach(async ({ page }) => {
  328 |         // 1. Navigasi ke SPA terlebih dahulu agar localStorage tersedia
  329 |         //    (localStorage hanya tersedia setelah halaman dimuat)
> 330 |         await page.goto(SPA_URL);
      |                    ^ Error: page.goto: Test ended.
  331 | 
  332 |         // 2. Bersihkan localStorage untuk memastikan state bersih
  333 |         await clearAuthTokens(page);
  334 |     });
  335 | 
  336 |     // =========================================================================
  337 |     // TEST CASE: AUTH-04
  338 |     // =========================================================================
  339 |     // JUDUL:
  340 |     //   Auth Guard: Akses dashboard tanpa token harus redirect ke login
  341 |     //
  342 |     // SKENARIO:
  343 |     //   Pengguna yang BELUM login (tidak memiliki access_token di localStorage)
  344 |     //   mencoba mengakses halaman #dashboard secara langsung melalui URL.
  345 |     //
  346 |     // EKSPEKTASI:
  347 |     //   Router SPA (handleRouting di router.js) mendeteksi tidak ada token
  348 |     //   dan melakukan redirect otomatis ke #login.
  349 |     //
  350 |     // REFERENSI KODE:
  351 |     //   Lihat router.js baris 133-138:
  352 |     //     } else {
  353 |     //         if (hash === '#dashboard') {
  354 |     //             window.location.hash = '#login';
  355 |     //             return;
  356 |     //         }
  357 |     //     }
  358 |     // =========================================================================
  359 |     test('AUTH-04: Akses #dashboard tanpa token → redirect ke #login', async ({ page }) => {
  360 |         // -------------------------------------------------------------------
  361 |         // LANGKAH 1: Pastikan localStorage benar-benar kosong (tidak ada token)
  362 |         // -------------------------------------------------------------------
  363 |         const tokenBefore = await page.evaluate(() => {
  364 |             // Jalankan di browser: cek apakah ada access_token
  365 |             return localStorage.getItem('access_token');
  366 |         });
  367 | 
  368 |         // Assertion: token harus null (tidak ada)
  369 |         expect(tokenBefore).toBeNull();
  370 | 
  371 |         // -------------------------------------------------------------------
  372 |         // LANGKAH 2: Navigasi langsung ke #dashboard (tanpa login)
  373 |         // -------------------------------------------------------------------
  374 |         // Ini mensimulasikan pengguna yang mengetik URL langsung di address bar
  375 |         // atau mengklik bookmark ke halaman dashboard.
  376 |         await page.goto(`${SPA_URL}#dashboard`);
  377 | 
  378 |         // -------------------------------------------------------------------
  379 |         // LANGKAH 3: Tunggu router SPA melakukan redirect
  380 |         // -------------------------------------------------------------------
  381 |         // page.waitForFunction() menunggu hingga kondisi tertentu terpenuhi
  382 |         // di dalam browser. Kita menunggu hash URL berubah menjadi '#login'.
  383 |         //
  384 |         await page.waitForFunction(
  385 |             () => window.location.hash === '#login',
  386 |             null,
  387 |             { timeout: 5000 }
  388 |         );
  389 | 
  390 |         // -------------------------------------------------------------------
  391 |         // LANGKAH 4: Verifikasi bahwa URL hash sekarang adalah #login
  392 |         // -------------------------------------------------------------------
  393 |         // expect(page).toHaveURL() memeriksa URL lengkap halaman saat ini.
  394 |         // Kita gunakan regex agar fleksibel dengan base URL.
  395 |         //
  396 |         await expect(page).toHaveURL(/#login/);
  397 | 
  398 |         // -------------------------------------------------------------------
  399 |         // LANGKAH 5: Verifikasi bahwa form login ditampilkan
  400 |         // -------------------------------------------------------------------
  401 |         // Ini adalah verifikasi tambahan: bukan hanya URL yang berubah,
  402 |         // tapi konten halaman juga harus menampilkan form login.
  403 |         //
  404 |         const loginForm = page.locator('#loginForm');
  405 |         await expect(loginForm).toBeVisible({ timeout: 5000 });
  406 | 
  407 |         // Cetak info debug ke console test (opsional, untuk debugging)
  408 |         console.log('[AUTH-04] ✅ Redirect dari #dashboard ke #login berhasil diverifikasi');
  409 |     });
  410 | 
  411 |     // =========================================================================
  412 |     // TEST CASE: AUTH-05
  413 |     // =========================================================================
  414 |     // JUDUL:
  415 |     //   Token Interceptor: Access token kadaluarsa → SPA menangani 401 error
  416 |     //
  417 |     // SKENARIO:
  418 |     //   Pengguna memiliki access_token yang sudah kadaluarsa (expired) namun
  419 |     //   refresh_token masih valid. Saat SPA melakukan API call dan mendapat
  420 |     //   respons 401, interceptor di api.js harus membersihkan localStorage
  421 |     //   dan mengarahkan pengguna ke halaman login.
  422 |     //
  423 |     // CATATAN TEKNIS:
  424 |     //   Dalam kode api.js (baris 28-33), interceptor sederhana diimplementasikan:
  425 |     //     if(response.status == 401){
  426 |     //         alert('Sesi Anda telah habis atau Anda belum login.');
  427 |     //         localStorage.clear();
  428 |     //         window.location.hash = '#login';
  429 |     //         return null;
  430 |     //     }
```