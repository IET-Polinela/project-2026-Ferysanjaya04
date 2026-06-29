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

// LAB 12: Fungsi Logout
window.logout = function() {
    console.log('Logout dimulai...');
    
    // Hapus token dari localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    console.log('Token dihapus dari localStorage');
    
    // Redirect ke halaman login
    alert('Anda telah logout!');
    window.location.hash = '#login';
    
    // Pastikan halaman reload
    setTimeout(function() {
        window.location.reload();
    }, 100);
}

// LAB 12: Fungsi Setup Form Register
function setupRegisterForm() {
    const registerForm = document.getElementById('registerForm');
    if (!registerForm) return;

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const passwordConfirm = document.getElementById('registerPasswordConfirm').value;

        // Validasi dari frontend
        if (password !== passwordConfirm) {
            alert('Password tidak cocok!');
            return;
        }

        if (password.length < 6) {
            alert('Password minimal 6 karakter!');
            return;
        }

        try {
            // Kirim ke endpoint /api/register/ di backend publik (samakan BASE_URL dengan API lain)
            const response = await fetch('http://103.151.63.85:8002/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password,
                    password_confirm: passwordConfirm
                })
            });

            if (response.ok) {
                const data = await response.json();
                alert(`✅ ${data.message}`);
                
                // Redirect ke login page
                window.location.hash = '#login';
                registerForm.reset();
            } else {
                const errorData = await response.json();
                
                // Tangani error messages dari backend
                let errorMsg = 'Pendaftaran Gagal: ';
                if (typeof errorData === 'object') {
                    // Jika error berbentuk object (field-specific errors)
                    for (const [key, value] of Object.entries(errorData)) {
                        if (Array.isArray(value)) {
                            errorMsg += `${key}: ${value.join(', ')} | `;
                        } else {
                            errorMsg += `${key}: ${value} | `;
                        }
                    }
                } else {
                    errorMsg += JSON.stringify(errorData);
                }
                
                alert(errorMsg);
            }
        } catch (error) {
            console.error('Register error:', error);
            alert('Gagal terhubung ke server backend Django!');
        }
    });
}