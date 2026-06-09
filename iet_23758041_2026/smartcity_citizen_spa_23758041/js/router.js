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
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <button class="btn btn-primary btn-lg w-100 fw-bold mb-3">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card border-0 p-5 shadow-sm text-center text-muted border-dashed" style="border: 2px dashed #dee2e6 !important;">
                    <i class="bi bi-inbox fs-1 text-primary"></i>
                    <h5 class="mt-3 fw-bold text-dark">Selamat Datang!</h5>
                    <p class="small">Koneksi API untuk data laporan akan diimplementasikan pada Lab 12.</p>
                </div>
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
    
    // Menyuntikkan template HTML ke dalam elemen main id 'app-content'
    document.getElementById('app-content').innerHTML = routes[hash] || routes['#login'];
    
    // Jika rute saat ini adalah #login, aktifkan penangkap form submit dari auth.js
    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }
}

// 3. Mendaftarkan Sensor Event Listener di Browser Warga
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);