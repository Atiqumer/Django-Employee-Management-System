# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    join_date = models.DateField()
    account = models.CharField(max_length=15)
    Address = models.CharField(max_length=55)
    acc_source = models.CharField(max_length=15)
    contract_file = models.FileField(upload_to='contracts/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    client = models.CharField(max_length=100)
    deadline = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employees = models.ManyToManyField(Employee, related_name="projects")
    status = models.CharField(max_length=20, choices=[("ongoing", "Ongoing"), ("completed", "Completed")])
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class SalarySlip(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, blank=True)
    month = models.CharField(max_length=20,default=None)
    salary_period = models.CharField(max_length=20, null=True, blank=True)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.net_salary = self.base_salary + self.allowances - self.deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.month}"

class Leave(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)  
    end_date = models.DateField(default=timezone.now)    
    reason = models.TextField() 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.employee.name} - {self.start_date} to {self.end_date}"

