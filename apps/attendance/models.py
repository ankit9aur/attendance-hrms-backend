from django.db import models
from apps.employees.models import Employee


class AttendanceRecord(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    date = models.DateField()

    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    work_hours = models.FloatField(default=0)
    overtime = models.FloatField(default=0)
    undertime = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=[
            ("PRESENT", "Present"),
            ("HALF", "Half Day"),
            ("ABSENT", "Absent"),
        ],
        default="ABSENT",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "date")
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["employee", "date"]),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"
