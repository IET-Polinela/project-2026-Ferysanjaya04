// ================================================================
// LAB 12 SOAL 5: Global Variable untuk Edit Report
// ================================================================
let editingReportId = null;

/**
 * setupReportModal()
 * LAB 12: Setup event listener untuk tombol "Simpan Draft" dan "Ajukan"
 */
window.setupReportModal = function() {
    const btnDraft = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');
    const reportModal = document.getElementById('reportModal');
    
    if (btnDraft) {
        btnDraft.addEventListener('click', handleSaveDraft);
    }
    
    if (btnSubmit) {
        btnSubmit.addEventListener('click', handleSubmitReport);
    }
    
    // LAB 12 SOAL 5: Reset form & editingReportId saat modal ditutup
    if (reportModal) {
        reportModal.addEventListener('hidden.bs.modal', function () {
            document.getElementById('reportForm').reset();
            document.getElementById('reportModalLabel').textContent = '✏️ Buat Laporan Baru';
            editingReportId = null;
        });
    }
}

/**
 * editDraft(id)
 * LAB 12 SOAL 5: Fungsi untuk edit laporan yang masih DRAFT
 * - Ambil data laporan dari API
 * - Isi form modal dengan data tersebut
 * - Set editingReportId = id
 * - Tampilkan modal
 */
window.editDraft = async function(id) {
    try {
        const response = await requestAPI(`/api/report/${id}/`, 'GET');
        
        // LAB 12 SOAL 5: Handle 401 Unauthorized
        if (response.status === 401) {
            alert('Session Anda telah expired. Silakan login kembali.');
            return;
        }
        
        if (response.ok) {
            const report = await response.json();
            
            // Isi form dengan data laporan lama
            document.getElementById('reportTitle').value = report.title;
            document.getElementById('reportCategory').value = report.category;
            document.getElementById('reportDescription').value = report.description;
            document.getElementById('reportLocation').value = report.location;
            
            // Set global variable editingReportId
            editingReportId = id;
            
            // Update modal title
            document.getElementById('reportModalLabel').textContent = '✏️ Edit Laporan Draft';
            
            // Tampilkan modal
            const modal = new bootstrap.Modal(document.getElementById('reportModal'));
            modal.show();
        } else {
            const errorData = await response.json();
            console.error('API Error:', errorData);
            alert(`Gagal mengambil data laporan: ${errorData.detail || response.status}`);
        }
    } catch (error) {
        console.error('Error editing draft:', error);
        alert('Gagal terhubung ke server! Cek console untuk detail error.');
    }
}

/**
 * handleSaveDraft()
 * LAB 12 SOAL 5: Submit form dengan status DRAFT
 * - Jika editingReportId == null → POST (create new)
 * - Jika editingReportId != null → PUT (update existing)
 */
window.handleSaveDraft = async function() {
    const reportForm = document.getElementById('reportForm');
    
    if (!reportForm.checkValidity()) {
        alert('Silakan lengkapi semua field!');
        return;
    }
    
    const formData = {
        title: document.getElementById('reportTitle').value,
        category: document.getElementById('reportCategory').value,
        description: document.getElementById('reportDescription').value,
        location: document.getElementById('reportLocation').value,
        status: 'DRAFT'
    };
    
    try {
        // Tentukan method dan endpoint berdasarkan editingReportId
        const method = editingReportId ? 'PUT' : 'POST';
        const endpoint = editingReportId ? `/api/report/${editingReportId}/` : '/api/report/';
        
        const response = await requestAPI(endpoint, method, formData);
        
        if (response.status === 201 || response.status === 200) {
            const statusText = editingReportId ? 'diperbarui' : 'disimpan';
            alert(`Laporan berhasil ${statusText} sebagai Draft!`);
            
            // Reset form
            reportForm.reset();
            
            // Reset modal title
            document.getElementById('reportModalLabel').textContent = '✏️ Buat Laporan Baru';
            
            // Reset global variable
            editingReportId = null;
            
            // Tutup modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('reportModal'));
            modal.hide();
            
            // Reload data dashboard
            loadDashboardData('my_reports', 1);
        } else {
            const error = await response.json();
            alert(`Gagal menyimpan draft: ${error.detail || 'Coba lagi nanti'}`);
        }
    } catch (error) {
        console.error('Error saving draft:', error);
        alert('Gagal terhubung ke server!');
    }
}

/**
 * handleSubmitReport()
 * LAB 12 SOAL 5: Submit form dengan status REPORTED
 * - Jika editingReportId == null → POST (create new)
 * - Jika editingReportId != null → PUT (update existing / submit draft)
 */
window.handleSubmitReport = async function() {
    const reportForm = document.getElementById('reportForm');
    
    if (!reportForm.checkValidity()) {
        alert('Silakan lengkapi semua field!');
        return;
    }
    
    const formData = {
        title: document.getElementById('reportTitle').value,
        category: document.getElementById('reportCategory').value,
        description: document.getElementById('reportDescription').value,
        location: document.getElementById('reportLocation').value,
        status: 'REPORTED'
    };
    
    try {
        // Tentukan method dan endpoint berdasarkan editingReportId
        const method = editingReportId ? 'PUT' : 'POST';
        const endpoint = editingReportId ? `/api/report/${editingReportId}/` : '/api/report/';
        
        const response = await requestAPI(endpoint, method, formData);
        
        if (response.status === 201 || response.status === 200) {
            const statusText = editingReportId ? 'diperbarui dan diajukan' : 'berhasil diajukan';
            alert(`Laporan ${statusText}! Terima kasih atas laporan Anda.`);
            
            // Reset form
            reportForm.reset();
            
            // Reset modal title
            document.getElementById('reportModalLabel').textContent = '✏️ Buat Laporan Baru';
            
            // Reset global variable
            editingReportId = null;
            
            // Tutup modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('reportModal'));
            modal.hide();
            
            // Reload data dashboard
            loadDashboardData('feed', 1);
        } else {
            const error = await response.json();
            alert(`Gagal mengajukan laporan: ${error.detail || 'Coba lagi nanti'}`);
        }
    } catch (error) {
        console.error('Error submitting report:', error);
        alert('Gagal terhubung ke server!');
    }
}

// ================================================================
// LAB 12: Fungsi Utama untuk Load Data Laporan dengan Pagination
// ================================================================
/**
 * loadSummaryStats()
 * LAB 12: Kalkulasi Rekap Status di Sidebar
 * Menggunakan "Bypass Pagination" dengan page_size besar untuk mengambil semua data.
 * Kemudian gunakan .filter().length untuk menghitung per status.
 */
window.loadSummaryStats = async function() {
    try {
        // Tembak API dengan page_size=1000 untuk bypass pagination & ambil semua data laporan milik user
        const response = await requestAPI(`/api/report/?tab=my_reports&page_size=1000`, 'GET');
        
        // LAB 12 SOAL 4: Handle 401 Unauthorized
        if (response.status === 401) {
            console.warn('Token tidak valid. Skip loading summary stats.');
            return;
        }
        
        if (response.ok) {
            const data = await response.json();
            const allReports = data.results || [];
            
            // Hitung jumlah laporan per status menggunakan .filter().length
            const draftCount = allReports.filter(r => r.status === 'DRAFT').length;
            const processingCount = allReports.filter(r => 
                r.status === 'REPORTED' || r.status === 'IN_PROGRESS'
            ).length;
            const completedCount = allReports.filter(r => 
                r.status === 'VERIFIED' || r.status === 'RESOLVED'
            ).length;
            const totalCount = allReports.length;
            
            // Update HTML sidebar dengan data statistik
            const summaryContainer = document.getElementById('summaryStats');
            if (summaryContainer) {
                summaryContainer.innerHTML = `
                    <div class="card border-0 shadow-sm">
                        <div class="card-body">
                            <h6 class="fw-bold text-primary mb-3">
                                <i class="bi bi-graph-up me-2"></i>Statistik Laporan
                            </h6>
                            <hr>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between mb-1">
                                    <small class="fw-bold">Total</small>
                                    <small class="text-primary fw-bold">${totalCount}</small>
                                </div>
                                <div class="progress" style="height: 6px;">
                                    <div class="progress-bar bg-primary" style="width: 100%"></div>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <div class="d-flex justify-content-between mb-1">
                                    <small class="fw-bold">Draft</small>
                                    <small class="text-secondary fw-bold">${draftCount}</small>
                                </div>
                                <div class="progress" style="height: 6px;">
                                    <div class="progress-bar bg-warning" style="width: ${totalCount > 0 ? (draftCount / totalCount * 100) : 0}%"></div>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <div class="d-flex justify-content-between mb-1">
                                    <small class="fw-bold">Diproses</small>
                                    <small class="text-info fw-bold">${processingCount}</small>
                                </div>
                                <div class="progress" style="height: 6px;">
                                    <div class="progress-bar bg-info" style="width: ${totalCount > 0 ? (processingCount / totalCount * 100) : 0}%"></div>
                                </div>
                            </div>
                            
                            <div class="mb-2">
                                <div class="d-flex justify-content-between mb-1">
                                    <small class="fw-bold">Selesai</small>
                                    <small class="text-success fw-bold">${completedCount}</small>
                                </div>
                                <div class="progress" style="height: 6px;">
                                    <div class="progress-bar bg-success" style="width: ${totalCount > 0 ? (completedCount / totalCount * 100) : 0}%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
        }
    } catch (error) {
        console.error('Error loading summary stats:', error);
    }
}

/**
 * loadDashboardData(tab, page)
 * Menembak API backend dengan parameter tab dan page, kemudian:
 * 1. Extract data paginasi dari response
 * 2. Render kartu laporan via renderList()
 * 3. Render tombol halaman via renderPagination()
 * 4. Load statistik sidebar via loadSummaryStats()
 */
window.loadDashboardData = async function(tab = 'feed', page = 1) {
    try {
        // Step 1: Tembak API dengan parameter tab dan page
        const response = await requestAPI(`/api/report/?tab=${tab}&page=${page}`, 'GET');
        
        // LAB 12 SOAL 4: Handle 401 Unauthorized
        if (response.status === 401) {
            alert('Session Anda telah expired. Silakan login kembali.');
            return;
        }
        
        if (response.ok) {
            const data = await response.json();
            
            // INSTRUKSI 1: Ekstraksi Data Paginasi (Destructuring)
            const allReports = data.results || [];           // Ambil array laporan dari response
            const totalCount = data.count || 0;               // Total laporan keseluruhan
            const pageSize = 10;                              // Sesuai konfigurasi backend
            const totalPages = Math.ceil(totalCount / pageSize); // Hitung total halaman
            
            // INSTRUKSI 2: Pembaruan UI dengan Memanggil Fungsi Lain
            // Fungsi 1: renderList() - Menggambar susunan kartu laporan
            renderList(allReports, tab);
            
            // Fungsi 2: renderPagination() - Menyusun tombol halaman
            renderPagination(totalPages, page, tab);
            
            // LAB 12 SOAL 4: Panggil loadSummaryStats() untuk update sidebar statistik
            loadSummaryStats();
            
        } else {
            const errorData = await response.json();
            document.getElementById('listContainer').innerHTML = `
                <div class="col-12 text-center text-muted border-dashed p-5" style="border: 2px dashed #dee2e6 !important;">
                    <i class="bi bi-exclamation-triangle fs-1 text-warning"></i>
                    <h5 class="mt-3 fw-bold text-dark">Gagal Memuat Data</h5>
                    <p class="small">${errorData.detail || 'Silakan coba lagi nanti.'}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        document.getElementById('listContainer').innerHTML = `
            <div class="col-12 text-center text-muted border-dashed p-5" style="border: 2px dashed #dee2e6 !important;">
                <i class="bi bi-cloud-exclamation fs-1 text-danger"></i>
                <h5 class="mt-3 fw-bold text-dark">Koneksi Gagal</h5>
                <p class="small">Tidak dapat terhubung ke server backend.</p>
            </div>
        `;
    }
}

/**
 * renderList(reports, tab)
 * Render daftar kartu laporan dengan Bootstrap 5 Cards
 * Nanti akan dilengkapi dengan Progress Bar berdasarkan status
 */
window.renderList = function(reports, tab) {
    const listContainer = document.getElementById('listContainer');
    
    if (!reports || reports.length === 0) {
        listContainer.innerHTML = `
            <div class="col-12 text-center text-muted border-dashed p-5" style="border: 2px dashed #dee2e6 !important;">
                <i class="bi bi-inbox fs-1 text-primary"></i>
                <h5 class="mt-3 fw-bold text-dark">Belum Ada Laporan</h5>
                <p class="small">Mulai dengan membuat laporan baru untuk kota Anda.</p>
            </div>
        `;
        return;
    }
    
    // Render setiap laporan sebagai kartu
    listContainer.innerHTML = reports.map(report => {
        console.log('Rendering report:', {id: report.id, title: report.title, status: report.status});
        
        return `
        <div class="col-12 col-md-6 col-lg-12">
            <div class="card border-0 shadow-sm h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title fw-bold text-dark">${report.title}</h5>
                        <span class="badge bg-primary">${report.get_category_display || report.category}</span>
                    </div>
                    <p class="card-text text-muted small">${report.description}</p>
                    <div class="d-flex gap-2 align-items-center mb-3">
                        <i class="bi bi-geo-alt text-danger"></i>
                        <small class="text-secondary">${report.location}</small>
                    </div>
                    
                    <!-- Status & Progress Bar akan ditambahkan di sini -->
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="badge bg-secondary">${report.status}</span>
                        <small class="text-muted">${new Date(report.updated_at).toLocaleDateString('id-ID')}</small>
                    </div>
                    
                    <!-- LAB 12 SOAL 5: Tombol Edit untuk Laporan DRAFT -->
                    ${report.status === 'DRAFT' ? `
                        <button type="button" class="btn btn-sm btn-outline-warning w-100" onclick="editDraft(${report.id})" data-report-id="${report.id}">
                            <i class="bi bi-pencil-square me-1"></i>Edit Draft
                        </button>
                    ` : ''}
                </div>
            </div>
        </div>
        `;
    }).join('');
}

/**
 * renderPagination(totalPages, currentPage, tab)
 * Render tombol navigasi halaman
 */
window.renderPagination = function(totalPages, currentPage, tab) {
    const paginationContainer = document.getElementById('paginationContainer');
    
    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }
    
    let paginationHTML = '<nav><ul class="pagination justify-content-center">';
    
    // Tombol Previous
    if (currentPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <button class="page-link" onclick="loadDashboardData('${tab}', ${currentPage - 1})">
                    <i class="bi bi-chevron-left"></i> Sebelumnya
                </button>
            </li>
        `;
    }
    
    // Tombol halaman
    for (let i = 1; i <= totalPages; i++) {
        if (i === currentPage) {
            paginationHTML += `
                <li class="page-item active">
                    <span class="page-link">${i}</span>
                </li>
            `;
        } else {
            paginationHTML += `
                <li class="page-item">
                    <button class="page-link" onclick="loadDashboardData('${tab}', ${i})">${i}</button>
                </li>
            `;
        }
    }
    
    // Tombol Next
    if (currentPage < totalPages) {
        paginationHTML += `
            <li class="page-item">
                <button class="page-link" onclick="loadDashboardData('${tab}', ${currentPage + 1})">
                    Selanjutnya <i class="bi bi-chevron-right"></i>
                </button>
            </li>
        `;
    }
    
    paginationHTML += '</ul></nav>';
    paginationContainer.innerHTML = paginationHTML;
}