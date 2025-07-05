# Create your views here.
def is_admin(user):
    return user.is_superuser or user.email in ['atiqumer15@gmail.com', 'shaheryartariq909@gmail.com']

def is_user(user):
    return not is_admin(user)

    
from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

@login_required
@user_passes_test(is_admin)
def employee_list(request):
    query = request.GET.get('q')
    if query:
        employees = Employee.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(designation__icontains=query)
        )
    else:
        employees = Employee.objects.all()
    return render(request, 'core/employee_list.html', {'employees': employees})

@login_required
@user_passes_test(is_admin)
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)  
        if form.is_valid():
            print("Valid form. Saving...")
            form.save()
            return redirect('employee_list')
        else:
            print("Form Errors:", form.errors)
    else:
        form = EmployeeForm()
    return render(request, 'core/add_employee.html', {'form': form})

from .models import Project
from .forms import ProjectForm

@login_required
def project_list(request):
    query = request.GET.get('q')

    if request.user.is_superuser or request.user.email in ['atiqumer15@gmail.com', 'shaheryartariq909@gmail.com']:
        projects = Project.objects.all()
    else:
        try:
            employee = Employee.objects.get(email=request.user.email)
            projects = Project.objects.filter(employees=employee)
        except Employee.DoesNotExist:
            projects = Project.objects.none()
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(status__icontains=query) |
            Q(employees__name__icontains=query) |
            Q(client__icontains=query)
        ).distinct()

    return render(request, 'core/project_list.html', {
    'projects': projects,
    'is_admin': is_admin(request.user)
})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'core/add_project.html', {'form': form})

from .models import SalarySlip
from .forms import SalarySlipForm
@login_required
def salary_list(request):
    query = request.GET.get('q')
    
    if is_admin(request.user):
        slips = SalarySlip.objects.all()
    else:
        try:
            employee = Employee.objects.get(email=request.user.email)
            slips = SalarySlip.objects.filter(employee=employee)
        except Employee.DoesNotExist:
            slips = SalarySlip.objects.none()

    if query:
        slips = slips.filter(
            Q(employee__name__icontains=query) |
            Q(month__icontains=query)
        )

    return render(request, 'core/salary_list.html', {
        'slips': slips,
        'is_admin': is_admin(request.user)
    })

@login_required
def add_salary(request):
    if request.method == 'POST':
        form = SalarySlipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salary_list')
    else:
        form = SalarySlipForm()
    return render(request, 'core/add_salary.html', {'form': form})

from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    user = request.user
    context = {
        'is_admin': is_admin(user),
        'is_normal_user': is_user(user),
    }

    try:
        employee = Employee.objects.get(email=user.email)
    except Employee.DoesNotExist:
        employee = None

    if is_admin(user):
        context.update({
            'total_employees': Employee.objects.count(),
            'total_projects': Project.objects.count(),
            'ongoing_projects': Project.objects.filter(status='ongoing').count(),
            'total_salary_slips': SalarySlip.objects.count(),
        })
    else:
        user_projects = Project.objects.filter(employees=employee) if employee else []
        user_salary_slips = SalarySlip.objects.filter(employee=employee) if employee else []
        user_leaves = Leave.objects.filter(employee=employee) if employee else []
        context.update({
            'employee': employee,
            'user_projects': user_projects,
            'user_salary_slips': user_salary_slips,
            'user_leaves': user_leaves,
        })

    return render(request, 'core/dashboard.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm

@login_required
@user_passes_test(is_admin)
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee details updated successfully.")
            return redirect('employee_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'core/edit_employee.html', {'form': form,'employee': employee})

@login_required
@user_passes_test(is_admin)
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list')  # Redirect to the employee list after deletion

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/edit_project.html', {'form': form})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project_list')

@login_required
def edit_salary(request, pk):
    salary = get_object_or_404(SalarySlip, pk=pk)
    if request.method == 'POST':
        form = SalarySlipForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            return redirect('salary_list')
    else:
        form = SalarySlipForm(instance=salary)
    return render(request, 'core/edit_salary.html', {'form': form})

@login_required
def delete_salary(request, pk):
    salary = get_object_or_404(SalarySlip, pk=pk)
    salary.delete()
    return redirect('salary_list')
    
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard') 
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  
    return redirect('login')  


from .models import Employee, Leave
@login_required
def public_employee_profile(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    leaves = Leave.objects.filter(employee=employee).order_by('-created_at')
    return render(request, 'core/employee_profile.html', {'employee': employee, 'leaves': leaves})



from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect   
@login_required
def delete_contract(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if employee.contract_file:
        employee.contract_file.delete(save=False)
        employee.contract_file = None
        employee.save()
        messages.success(request, "Contract file deleted successfully.")
    else:
        messages.warning(request, "No contract file found.")

    return redirect('edit_employee', pk=pk)

from django.shortcuts import render, redirect
from .forms import LeaveForm
from .models import Leave
from django.core.mail import send_mail
from django.conf import settings
@login_required
def leave_management(request):
    employee = None

    if not request.user.is_superuser:
        try:
            employee = request.user.employee
            print("Logged-in user:", request.user)
            print("Is superuser:", request.user.is_superuser)
            print("Employee found:", request.user.employee)
        except Employee.DoesNotExist:
            messages.error(request,"You are not linked to an employee profile.")
            return redirect('dashboard')

    if request.method == 'POST':
        if request.user.is_superuser:
            form = LeaveForm(request.POST)
        else:
            form = LeaveForm(request.POST)
            form.fields.pop('employee', None)

        if form.is_valid():
            leave = form.save(commit=False)
            if not request.user.is_superuser:
                leave.employee = employee
            leave.save()

            if not request.user.is_superuser:
                send_mail(
                    subject='New Leave Request Submitted',
                    message=f"Employee: {employee.name}\nFrom: {leave.start_date} To: {leave.end_date}\nReason: {leave.reason}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['shaheryar@neuralflex.io'],  # Replace with your admin email
                    fail_silently=True,
                )
            messages.success(request, "Leave successfully submitted.")
            return redirect('leave-management')
    else:
        form = LeaveForm()
        if not request.user.is_superuser:
            form.fields.pop('employee', None)

    query = request.GET.get('q')
    if request.user.is_superuser:
        leaves = Leave.objects.select_related('employee').order_by('-start_date')
        if query:
            leaves = leaves.filter(employee__name__icontains=query)
    else:
        leaves = Leave.objects.filter(employee=employee).order_by('-start_date')

    return render(request, 'core/leave_management.html', {
        'form': form,
        'leaves': leaves,
        'query': query,
        'is_admin': request.user.is_superuser,
    })


@login_required
def delete_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    if request.user.is_superuser or leave.employee.user == request.user:
        leave.delete()
        messages.success(request, "Leave deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this leave.")

    return redirect('leave-management')


from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from .models import Leave

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


@login_required
@admin_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'approved'
    leave.save()
    send_mail(
        'Leave Approved',
        f'Dear {leave.employee.name}, your leave from {leave.start_date} to {leave.end_date} has been approved.',
        settings.EMAIL_HOST_USER,
        [leave.employee.user.email],
        fail_silently=True,
    )
    messages.success(request, 'Leave approved successfully.')
    return redirect('leave-management')


@login_required
@admin_required
def reject_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'rejected'
    leave.save()
    send_mail(
        'Leave Rejected',
        f'Dear {leave.employee.name}, your leave from {leave.start_date} to {leave.end_date} has been rejected.',
        settings.EMAIL_HOST_USER,
        [leave.employee.user.email],
        fail_silently=True,
    )
    messages.warning(request, 'Leave rejected.')
    return redirect('leave-management')



from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import LETTER, A4, A5, LEGAL, landscape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
import calendar
from datetime import datetime
from reportlab.platypus import Image
from django.conf import settings
from .models import SalarySlip

@login_required
def generate_payslip_pdf(request, slip_id):
    slip = get_object_or_404(SalarySlip, id=slip_id)

    if not request.user.is_superuser and slip.employee.user != request.user:
        return redirect('dashboard')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=Payslip_{slip.employee.name}_{slip.month}.pdf'

    doc = SimpleDocTemplate(response, pagesize=LETTER, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    story = []

    # Load logo
    logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=135, height=90)
        logo.hAlign = 'LEFT'
        story.append(logo)
        story.append(Spacer(1, 2))
    else:
        story.append(Paragraph("Logo not found at: " + logo_path, styles['Normal']))


    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Heading2'],
        alignment=TA_CENTER,  # center
        fontSize=16,
        leading=20,                  # Spacing between lines
        spaceAfter=16, 
        textColor=colors.HexColor("#333333"),
        fontName='Helvetica-Bold'
    )
    company_info = Paragraph(
        "<b>NeuralFlex </b><br/>"
        "304, Upper Mall Scheme,<br/>" 
        "Lahore, Pakistan",
        company_style
    )
    story.append(company_info)

    # Title
    title_style = ParagraphStyle('title', parent=styles['Title'], alignment=1, fontSize=19, spaceAfter=10)
    story.append(Paragraph("Salary Slip", title_style))


    try:
        salary_month = datetime.strptime(slip.month, "%B %Y")  # e.g., "June 2025"
        _, last_day = calendar.monthrange(salary_month.year, salary_month.month)
        salary_period = f"{salary_month.strftime('%d-%m-%Y')} to {salary_month.replace(day=last_day).strftime('%d-%m-%Y')}"
    except ValueError:
        salary_period = "N/A"
    # Employee Details Table
    emp_data = [
        ['Employee Name', slip.employee.name],
        ['Email', slip.employee.email],
        ['Designation', slip.employee.designation],
        ['Joining Date', str(slip.employee.join_date)],
        ['Account No', slip.employee.account],
        ['Bank', slip.employee.acc_source],
        ['Month', slip.month],
        ['Salary Period',slip.salary_period],
    ]
    emp_table = Table(emp_data, colWidths=[160, 320])
    emp_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.extend([emp_table, Spacer(1, 12)])

    # Salary Info Table
    net_pay = slip.base_salary + slip.allowances - slip.deductions
    salary_data = [
        ['Base Salary', f"PKR {slip.base_salary}"],
        ['Allowances', f"PKR {slip.allowances}"],
        ['Deductions', f"PKR {slip.deductions}"],
        ['Net Pay', f"PKR {net_pay}"],
    ]
    salary_table = Table(salary_data, colWidths=[160, 320])
    salary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.black),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.extend([salary_table, Spacer(1, 20)])
    # Footer
    footer_style = ParagraphStyle('footer', parent=styles['Normal'], fontSize=9, alignment=1, textColor=colors.grey)
    footer = Paragraph("This is a system-generated salary slip. No signature required.", footer_style)
    story.append(footer)

    doc.build(story)
    return response

