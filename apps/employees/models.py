from django.db import models
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)

    employee_code = models.CharField(max_length=50, unique=True)

    joining_date = models.DateField(default=timezone.now)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["employee_code"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.employee_code})"