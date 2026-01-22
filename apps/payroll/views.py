from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.employees.models import Employee
from .models import PayrollSummary
from .serializers import PayrollSummarySerializer
from .services import build_payroll_summary


class GeneratePayrollView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        month = request.GET.get("month")

        if not month:
            return Response({"detail": "month required"}, status=400)

        results = []

        for emp in Employee.objects.filter(is_active=True):
            data = build_payroll_summary(emp, month)

            obj, _ = PayrollSummary.objects.update_or_create(
                employee=emp,
                month=month,
                defaults=data,
            )

            results.append(obj)

        serializer = PayrollSummarySerializer(results, many=True)
        return Response(serializer.data)


class MonthlyPayrollView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.GET.get("month")

        qs = PayrollSummary.objects.filter(month=month).select_related("employee")
        serializer = PayrollSummarySerializer(qs, many=True)
        return Response(serializer.data)
