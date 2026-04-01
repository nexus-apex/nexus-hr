from django.contrib import admin
from .models import Employee, Department, LeaveRequest

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "department", "designation", "salary", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "email", "department"]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "head", "location", "budget", "employee_count", "created_at"]
    search_fields = ["name", "head", "location"]

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ["employee_name", "leave_type", "start_date", "end_date", "status", "created_at"]
    list_filter = ["leave_type", "status"]
    search_fields = ["employee_name"]
