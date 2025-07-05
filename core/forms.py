from django import forms
from .models import Employee
from .models import Leave
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'})
        }
        def save(self, commit=True):
            employee = super().save(commit=False)
            if not employee.user: 
                try:
                    user = User.objects.get(email=employee.email)
                    employee.user = user
                except User.DoesNotExist:
                    employee.user = None  
            if commit:
                employee.save()
                self.save_m2m()
            return employee

from .models import Project
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'employees': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

from .models import SalarySlip
class SalarySlipForm(forms.ModelForm):
    month = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = SalarySlip
        fields = ['employee', 'month','salary_period', 'base_salary', 'allowances', 'deductions']


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
