function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // WAJIB: Mencegah reload halaman dan kebocoran password

        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        try {
            // Kirim payload ke endpoint /api/token/ menggunakan requestAPI
            const response = await requestAPI('/api/token/', 'POST', {
                username: usernameInput,
                password: passwordInput
            });

            // Jika respons berstatus 200 (Sukses)
            if (response.ok) {
                const data = await response.json();
                
                // Simpan access dan refresh token ke dalam localStorage
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);

                // Berikan alert sukses
                alert('Login Berhasil! Selamat Datang di Citizen Portal.');
                
                // Ubah rute halaman secara instan ke dashboard
                window.location.hash = '#dashboard';
            } else {
                const errorData = await response.json();
                alert(`Login Gagal: ${errorData.detail || 'Username atau Password salah!'}`);
            }
        } catch (error) {
            alert('Gagal terhubung ke server backend Django!');
        }
    });
}