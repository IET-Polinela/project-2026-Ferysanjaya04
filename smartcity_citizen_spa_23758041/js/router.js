// 1. Konfigurasi Objek Rute Halaman menggunakan Template Literal Backtick (`)
const routes = {
    '#login': `
        <div class="row justify-content-center mt-5">
            <div class="col-md-4 card shadow-sm border-0 p-4">
                <h4 class="text-center fw-bold mb-4 text-primary">
                    <i class="bi bi-person-lock me-2"></i>Login Warga
                </h4>
                <form id="loginForm">
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" id="loginUsername" class="form-control" placeholder="Username" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" id="loginPassword" class="form-control mb-3" placeholder="Password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 fw-bold">
                        <i class="bi bi-box-arrow-in-right me-2"></i>Masuk
                    </button>
                </form>
                <hr>
                <p class="text-center text-muted small">Belum punya akun? 
                    <a href="#register" class="text-primary fw-bold text-decoration-none">Daftar di sini</a>
                </p>
            </div>
        </div>
    `,
    '#register': `
        <div class="row justify-content-center mt-5">
            <div class="col-md-5 card shadow-sm border-0 p-4">
                <h4 class="text-center fw-bold mb-4 text-primary">
                    <i class="bi bi-person-plus-fill me-2"></i>Daftar Akun Baru
                </h4>
                <form id="registerForm">
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" id="registerUsername" class="form-control" placeholder="Masukkan username" required>
                        <small class="text-muted">Min. 3 karakter, tanpa spasi</small>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email (Gmail)</label>
                        <input type="email" id="registerEmail" class="form-control" placeholder="email@gmail.com" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" id="registerPassword" class="form-control" placeholder="Min. 6 karakter" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Konfirmasi Password</label>
                        <input type="password" id="registerPasswordConfirm" class="form-control" placeholder="Ketik ulang password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 fw-bold">
                        <i class="bi bi-person-plus me-2"></i>Daftar Sekarang
                    </button>
                </form>
                <hr>
                <p class="text-center text-muted small">Sudah punya akun? 
                    <a href="#login" class="text-primary fw-bold text-decoration-none">Login di sini</a>
                </p>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <button id="btnBukaModal" class="btn btn-primary btn-lg w-100 fw-bold mb-3" data-bs-toggle="modal" data-bs-target="#reportModal">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                    <hr>
                    <div class="btn-group d-flex flex-column gap-2 w-100" role="group">
                        <button id="tabLaporanSaya" type="button" class="btn btn-outline-primary fw-bold" onclick="loadDashboardData('my_reports', 1)">
                            <i class="bi bi-file-earmark-text me-2"></i>Laporan Saya
                        </button>
                        <button id="tabFeedKota" type="button" class="btn btn-outline-primary fw-bold" onclick="loadDashboardData('feed', 1)">
                            <i class="bi bi-newspaper me-2"></i>Feed Kota
                        </button>
                    </div>
                </div>
                
                <!-- LAB 12 SOAL 4: Container untuk Statistik Laporan -->
                <div id="summaryStats" class="mt-3">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body text-center text-muted">
                            <i class="bi bi-hourglass-split fs-3"></i>
                            <p class="small mt-2">Loading statistik...</p>
                        </div>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div id="listContainer" class="row g-3">
                    <div class="col-12 text-center text-muted border-dashed p-5" style="border: 2px dashed #dee2e6 !important;">
                        <i class="bi bi-inbox fs-1 text-primary"></i>
                        <h5 class="mt-3 fw-bold text-dark">Selamat Datang!</h5>
                        <p class="small">Klik "Feed Kota" untuk melihat laporan dari warga lain.</p>
                    </div>
                </div>
                
                <div id="paginationContainer" class="mt-4"></div>
            </section>

            <aside class="col-lg-3 d-none d-lg-block">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <h6 class="fw-bold text-primary">
                        <i class="bi bi-info-circle-fill me-2"></i>Pengumuman
                    </h6>
                    <hr>
                    <p class="small text-muted">Selamat datang di sistem Citizen Portal Smart City Tracker lokal.</p>
                </div>
            </aside>
        </div>
    `
};

// 2. Fungsi Utama Pengatur Rute Halaman secara Instan
function handleRouting() {
    // Membaca hash URL aktif saat ini, jika kosong default mengarah ke '#login'
    const hash = window.location.hash || '#login';
    
    // 🔐 AUTH GUARD: Proteksi halaman dashboard dari akses tanpa token
    if (hash === '#dashboard') {
        const token = localStorage.getItem('access_token');
        if (!token) {
            // Redirect ke login jika tidak ada token
            window.location.hash = '#login';
            return;
        }
    }
    
    // LAB 12: Render navbar dinamis berdasarkan rute
    const navMenusContainer = document.getElementById('nav-menus');
    if (hash === '#dashboard') {
        // Tampilkan tombol logout di dashboard
        navMenusContainer.innerHTML = `
            <button id="logoutBtn" class="btn btn-outline-light btn-sm fw-bold">
                <i class="bi bi-box-arrow-right me-2"></i>Logout
            </button>
        `;
        // Attach event listener ke tombol logout
        document.getElementById('logoutBtn').addEventListener('click', function() {
            logout();
        });
    } else {
        // Sembunyikan menu navbar di login
        navMenusContainer.innerHTML = '';
    }
    
    // Menyuntikkan template HTML ke dalam elemen main id 'app-content'
    document.getElementById('app-content').innerHTML = routes[hash] || routes['#login'];
    
    // Jika rute saat ini adalah #login, aktifkan penangkap form submit dari auth.js
    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }
    
    // LAB 12: Jika rute saat ini adalah #register, aktifkan penangkap form submit untuk register
    if (hash === '#register' && typeof setupRegisterForm === 'function') {
        setupRegisterForm();
    }
    
    // LAB 12: Jika rute saat ini adalah #dashboard, load data dengan tab 'feed' halaman 1
    if (hash === '#dashboard' && typeof loadDashboardData === 'function') {
        loadDashboardData('feed', 1);
        
        // LAB 12 SOAL 5: Setup event listener untuk modal form
        if (typeof setupReportModal === 'function') {
            setupReportModal();
        }
    }
}

// 3. Mendaftarkan Sensor Event Listener di Browser Warga
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);

// Initial routing saat router.js selesai load
handleRouting();
