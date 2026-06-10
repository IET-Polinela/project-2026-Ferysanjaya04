"""
LAB 12: Custom Pagination Class
Memungkinkan client untuk override page_size melalui query parameter ?page_size=1000
"""

from rest_framework.pagination import PageNumberPagination


class ReportPagination(PageNumberPagination):
    """
    Custom PageNumberPagination yang mendukung parameter page_size di URL.
    Contoh: /api/report/?page_size=1000 akan mengembalikan 1000 item per halaman.
    
    Ini digunakan untuk "Bypass Pagination" pada Soal 4 - Kalkulasi Rekap Status.
    Dengan menggunakan page_size=1000, semua data dapat diambil dalam satu request.
    """
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Nama query parameter untuk override
    max_page_size = 10000  # Maksimal page_size yang diizinkan (safety limit)
