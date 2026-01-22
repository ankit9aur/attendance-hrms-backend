from django.urls import path
from .views import (
    DailyBulkAttendanceView,
    DailyAttendanceView,
    MonthlyAttendanceView,
    BiometricUploadAttendanceView,
)

urlpatterns = [
    # HR enters attendance for a day (bulk)
    path("bulk-entry/", DailyBulkAttendanceView.as_view(), name="bulk_attendance"),

    # Biometric CSV upload (bulk by employee_code)
    path("biometric-upload/", BiometricUploadAttendanceView.as_view(), name="biometric_upload"),

    # View daily attendance
    path("daily/", DailyAttendanceView.as_view(), name="daily_attendance"),

    # Monthly report
    path("monthly/", MonthlyAttendanceView.as_view(), name="monthly_attendance"),
]
