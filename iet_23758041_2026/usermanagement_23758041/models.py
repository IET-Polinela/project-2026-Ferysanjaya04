from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Field tambahan sesuai instruksi Lab 6
    # Bagian [cite] sudah dihapus agar tidak Error
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)

    def __str__(self):
        return self.username