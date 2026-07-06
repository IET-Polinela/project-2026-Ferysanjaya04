const BASE_URL = "http://103.151.63.85:8002"  // Server backend Django lokal

// Fungsi universal untuk fetch API ke Backend Django
async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    // Otomatis ambil access_token dari localStorage jika ada
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const config = {
        method: method,
        headers: headers
    };

    // Jika ada data body (seperti payload username & password)
    if (bodyData) {
        config.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, config);
        
        // LAB 12 SOAL 4: Handle 401 Unauthorized (Token Invalid/Expired)
        if (response.status === 401) {
            console.warn('Token tidak valid atau expired. Redirect ke login...');
            localStorage.clear();
            window.location.hash = '#login';
            return response;
        }
        
        return response;
    } catch (error) {
        console.error('Network Error:', error);
        throw error;
    }
}
