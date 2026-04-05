from django.db import models

class Report(models.Model):
    STATUS_CHOICES = [
        ('REPORTED', 'Dilaporkan'),
        ('IN_PROGRESS', 'Sedang Diproses'),
        ('RESOLVED', 'Selesai'),
        ('REJECTED', 'Ditolak'),
    ]
    
    CATEGORY_CHOICES = [
        ('JALAN', 'Jalan Rusak'),
        ('LAMPU', 'Lampu Jalan'),
        ('AIR', 'Pipa Air'),
        ('SAMPAH', 'Penumpukan Sampah'),
        ('LAINNYA', 'Lainnya'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='LAINNYA')
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
