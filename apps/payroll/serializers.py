from rest_framework import serializers
from .models import PayrollSummary


class PayrollSummarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)

    class Meta:
        model = PayrollSummary
        fields = "__all__"
