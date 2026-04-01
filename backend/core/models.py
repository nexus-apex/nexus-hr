from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    department = models.CharField(max_length=255, blank=True, default="")
    designation = models.CharField(max_length=255, blank=True, default="")
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    join_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("on_leave", "On Leave"), ("resigned", "Resigned"), ("terminated", "Terminated")], default="active")
    phone = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    head = models.CharField(max_length=255, blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employee_count = models.IntegerField(default=0)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    employee_name = models.CharField(max_length=255)
    leave_type = models.CharField(max_length=50, choices=[("casual", "Casual"), ("sick", "Sick"), ("earned", "Earned"), ("maternity", "Maternity"), ("comp_off", "Comp Off")], default="casual")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending")
    reason = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.employee_name
