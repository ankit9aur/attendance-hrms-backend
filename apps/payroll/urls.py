from django.urls import path
from .views import GeneratePayrollView, MonthlyPayrollView

urlpatterns = [
    # Generate payroll from attendance
    path("generate/", GeneratePayrollView.as_view(), name="generate_payroll"),

    # View payroll summary
    path("monthly/", MonthlyPayrollView.as_view(), name="monthly_payroll"),
]
