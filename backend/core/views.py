import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Employee, Department, LeaveRequest


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['employee_count'] = Employee.objects.count()
    ctx['employee_active'] = Employee.objects.filter(status='active').count()
    ctx['employee_on_leave'] = Employee.objects.filter(status='on_leave').count()
    ctx['employee_resigned'] = Employee.objects.filter(status='resigned').count()
    ctx['employee_total_salary'] = Employee.objects.aggregate(t=Sum('salary'))['t'] or 0
    ctx['department_count'] = Department.objects.count()
    ctx['department_total_budget'] = Department.objects.aggregate(t=Sum('budget'))['t'] or 0
    ctx['leaverequest_count'] = LeaveRequest.objects.count()
    ctx['leaverequest_casual'] = LeaveRequest.objects.filter(leave_type='casual').count()
    ctx['leaverequest_sick'] = LeaveRequest.objects.filter(leave_type='sick').count()
    ctx['leaverequest_earned'] = LeaveRequest.objects.filter(leave_type='earned').count()
    ctx['recent'] = Employee.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def employee_list(request):
    qs = Employee.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'employee_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def employee_create(request):
    if request.method == 'POST':
        obj = Employee()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.department = request.POST.get('department', '')
        obj.designation = request.POST.get('designation', '')
        obj.salary = request.POST.get('salary') or 0
        obj.join_date = request.POST.get('join_date') or None
        obj.status = request.POST.get('status', '')
        obj.phone = request.POST.get('phone', '')
        obj.save()
        return redirect('/employees/')
    return render(request, 'employee_form.html', {'editing': False})


@login_required
def employee_edit(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.department = request.POST.get('department', '')
        obj.designation = request.POST.get('designation', '')
        obj.salary = request.POST.get('salary') or 0
        obj.join_date = request.POST.get('join_date') or None
        obj.status = request.POST.get('status', '')
        obj.phone = request.POST.get('phone', '')
        obj.save()
        return redirect('/employees/')
    return render(request, 'employee_form.html', {'record': obj, 'editing': True})


@login_required
def employee_delete(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/employees/')


@login_required
def department_list(request):
    qs = Department.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = ''
    return render(request, 'department_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def department_create(request):
    if request.method == 'POST':
        obj = Department()
        obj.name = request.POST.get('name', '')
        obj.head = request.POST.get('head', '')
        obj.location = request.POST.get('location', '')
        obj.budget = request.POST.get('budget') or 0
        obj.employee_count = request.POST.get('employee_count') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/departments/')
    return render(request, 'department_form.html', {'editing': False})


@login_required
def department_edit(request, pk):
    obj = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.head = request.POST.get('head', '')
        obj.location = request.POST.get('location', '')
        obj.budget = request.POST.get('budget') or 0
        obj.employee_count = request.POST.get('employee_count') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/departments/')
    return render(request, 'department_form.html', {'record': obj, 'editing': True})


@login_required
def department_delete(request, pk):
    obj = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/departments/')


@login_required
def leaverequest_list(request):
    qs = LeaveRequest.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(employee_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(leave_type=status_filter)
    return render(request, 'leaverequest_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def leaverequest_create(request):
    if request.method == 'POST':
        obj = LeaveRequest()
        obj.employee_name = request.POST.get('employee_name', '')
        obj.leave_type = request.POST.get('leave_type', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.status = request.POST.get('status', '')
        obj.reason = request.POST.get('reason', '')
        obj.save()
        return redirect('/leaverequests/')
    return render(request, 'leaverequest_form.html', {'editing': False})


@login_required
def leaverequest_edit(request, pk):
    obj = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        obj.employee_name = request.POST.get('employee_name', '')
        obj.leave_type = request.POST.get('leave_type', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.status = request.POST.get('status', '')
        obj.reason = request.POST.get('reason', '')
        obj.save()
        return redirect('/leaverequests/')
    return render(request, 'leaverequest_form.html', {'record': obj, 'editing': True})


@login_required
def leaverequest_delete(request, pk):
    obj = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/leaverequests/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['employee_count'] = Employee.objects.count()
    data['department_count'] = Department.objects.count()
    data['leaverequest_count'] = LeaveRequest.objects.count()
    return JsonResponse(data)
