from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Employee, Department, LeaveRequest
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusHR with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexushr.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Employee.objects.count() == 0:
            for i in range(10):
                Employee.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    department=f"Sample {i+1}",
                    designation=f"Sample {i+1}",
                    salary=round(random.uniform(1000, 50000), 2),
                    join_date=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["active", "on_leave", "resigned", "terminated"]),
                    phone=f"+91-98765{43210+i}",
                )
            self.stdout.write(self.style.SUCCESS('10 Employee records created'))

        if Department.objects.count() == 0:
            for i in range(10):
                Department.objects.create(
                    name=f"Sample Department {i+1}",
                    head=f"Sample {i+1}",
                    location=f"Sample {i+1}",
                    budget=round(random.uniform(1000, 50000), 2),
                    employee_count=random.randint(1, 100),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Department records created'))

        if LeaveRequest.objects.count() == 0:
            for i in range(10):
                LeaveRequest.objects.create(
                    employee_name=f"Sample LeaveRequest {i+1}",
                    leave_type=random.choice(["casual", "sick", "earned", "maternity", "comp_off"]),
                    start_date=date.today() - timedelta(days=random.randint(0, 90)),
                    end_date=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["pending", "approved", "rejected"]),
                    reason=f"Sample reason for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 LeaveRequest records created'))
