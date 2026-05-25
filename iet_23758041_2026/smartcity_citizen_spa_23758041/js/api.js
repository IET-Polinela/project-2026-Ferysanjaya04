const BASE_URL = 'http://127.0.0.1:8000';

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
        return response;
    } catch (error) {
        console.error('Network Error:', error);
        throw error;
    }
}