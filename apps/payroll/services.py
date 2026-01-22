from apps.attendance.models import AttendanceRecord


def build_payroll_summary(employee, month):
    qs = AttendanceRecord.objects.filter(employee=employee, date__startswith=month)

    total_hours = sum(x.work_hours for x in qs)
    total_ot = sum(x.overtime for x in qs)
    total_ut = sum(x.undertime for x in qs)

    present = qs.filter(status="PRESENT").count()
    half = qs.filter(status="HALF").count()
    absent = qs.filter(status="ABSENT").count()

    return {
        "total_work_hours": round(total_hours, 2),
        "total_overtime": round(total_ot, 2),
        "total_undertime": round(total_ut, 2),
        "present_days": present,
        "half_days": half,
        "absent_days": absent,
    }
