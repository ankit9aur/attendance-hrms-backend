from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.employees.models import Employee
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer
from .services import calculate_attendance


# =====================================================
# MANUAL DAILY BULK ENTRY (HR FORM)
# =====================================================
class DailyBulkAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        date_str = request.data.get("date")
        entries = request.data.get("entries", [])

        if not date_str:
            return Response({"detail": "date is required"}, status=400)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Invalid date format"}, status=400)

        results = []

        for e in entries:
            emp_id = e.get("employee_id")
            check_in = e.get("check_in")
            check_out = e.get("check_out")

            try:
                employee = Employee.objects.get(id=emp_id, is_active=True)
            except Employee.DoesNotExist:
                continue

            work, ot, ut, status_val, in_t, out_t = calculate_attendance(check_in, check_out)

            obj, _ = AttendanceRecord.objects.update_or_create(
                employee=employee,
                date=date,
                defaults={
                    "check_in": in_t,
                    "check_out": out_t,
                    "work_hours": work,
                    "overtime": ot,
                    "undertime": ut,
                    "status": status_val,
                },
            )

            results.append(obj)

        serializer = AttendanceRecordSerializer(results, many=True)
        return Response(serializer.data, status=200)


# =====================================================
# BIOMETRIC CSV BULK UPLOAD (AUTO CREATE EMPLOYEE)
# =====================================================
class BiometricUploadAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        date_str = request.data.get("date")
        entries = request.data.get("entries", [])

        if not date_str:
            return Response({"detail": "date is required"}, status=400)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Invalid date format"}, status=400)

        created_employees = 0
        saved_attendance = 0
        skipped = []

        for e in entries:
            code = e.get("employee_code")
            name = e.get("employee_name") or "Unknown"
            designation = e.get("designation") or "Employee"
            check_in = e.get("check_in")
            check_out = e.get("check_out")

            if not code:
                skipped.append({"reason": "missing_employee_code", "row": e})
                continue

            employee, created = Employee.objects.get_or_create(
                employee_code=code,
                defaults={
                    "name": name,
                    "designation": designation,
                    "is_active": True,
                },
            )

            if created:
                created_employees += 1

            work, ot, ut, status_val, in_t, out_t = calculate_attendance(check_in, check_out)

            AttendanceRecord.objects.update_or_create(
                employee=employee,
                date=date,
                defaults={
                    "check_in": in_t,
                    "check_out": out_t,
                    "work_hours": work,
                    "overtime": ot,
                    "undertime": ut,
                    "status": status_val,
                },
            )

            saved_attendance += 1

        return Response(
            {
                "created_employees": created_employees,
                "saved_attendance": saved_attendance,
                "skipped": skipped,
            },
            status=200,
        )


# =====================================================
# VIEW DAILY ATTENDANCE
# =====================================================
class DailyAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.GET.get("date")

        if not date_str:
            return Response({"detail": "date is required"}, status=400)

        records = AttendanceRecord.objects.filter(date=date_str).select_related("employee")
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)


# =====================================================
# VIEW MONTHLY ATTENDANCE
# =====================================================
class MonthlyAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.GET.get("month")  # YYYY-MM

        if not month:
            return Response({"detail": "month is required"}, status=400)

        records = AttendanceRecord.objects.filter(date__startswith=month).select_related("employee")
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)
