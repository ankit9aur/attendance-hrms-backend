from django.db import models
from apps.employees.models import Employee


class PayrollSummary(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payroll_summaries",
    )

    month = models.CharField(max_length=7)  # YYYY-MM

    total_work_hours = models.FloatField(default=0)
    total_overtime = models.FloatField(default=0)
    total_undertime = models.FloatField(default=0)

    present_days = models.IntegerField(default=0)
    half_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)

    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "month")
        indexes = [
            models.Index(fields=["month"]),
            models.Index(fields=["employee", "month"]),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.month}"
