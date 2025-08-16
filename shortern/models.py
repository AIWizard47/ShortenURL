# models.py
import random
import string
from django.db import models
from django.utils import timezone

def generate_code(length=6):
    chars = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choices(chars, k=length))

class ShortURL(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=6, unique=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    def save(self, *args, **kwargs):
        # Auto-generate unique 6-char code if not set
        if not self.short_code:
            self.short_code = self._create_unique_code()
        super().save(*args, **kwargs)

    @classmethod
    def _create_unique_code(cls, length=6, max_tries=20):
        # Try several times to avoid rare collisions
        for _ in range(max_tries):
            code = generate_code(length)
            if not cls.objects.filter(short_code=code).exists():
                return code
        # Fallback: extend length if collisions persist
        while True:
            length += 1
            code = generate_code(length)
            if not cls.objects.filter(short_code=code).exists():
                return code
