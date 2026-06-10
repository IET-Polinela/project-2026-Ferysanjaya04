from django.db import models
from django.conf import settings


class Report(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    CATEGORY_CHOICES = [
        ('JALAN', 'Jalan Rusak'),
        ('LAMPU', 'Lampu Jalan'),
        ('AIR', 'Pipa Air'),
        ('SAMPAH', 'Penumpukan Sampah'),
        ('LAINNYA', 'Lainnya'),
        ('ALL', 'Semua Kategori'),
    ]

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='LAINNYA'
    )

    description = models.TextField()

    location = models.CharField(max_length=200)

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"