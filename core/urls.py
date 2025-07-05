from django.urls import path
from . import views

urlpatterns = [
    # Employee Views
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/<int:pk>/edit/', views.edit_employee, name='edit_employee'),
    path('employee/<int:pk>/delete/', views.delete_employee, name='delete_employee'),
    
    # Project Views
    path('projects/', views.project_list, name='project_list'),
    path('project/add/', views.add_project, name='add_project'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),

    # Salary Slip Views
    path('salary-slips/', views.salary_list, name='salary_list'),
    path('salary-slip/add/', views.add_salary, name='add_salary'),
    path('salary-slip/<int:pk>/edit/', views.edit_salary, name='edit_salary'),
    path('salary-slip/<int:pk>/delete/', views.delete_salary, name='delete_salary'),
    # Dashboard
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


   path('employee/<int:pk>/profile/', views.public_employee_profile, name='employee_profile'),
   path('employee/<int:pk>/delete-contract/', views.delete_contract, name='delete_contract'),
   path('leave/', views.leave_management, name='leave-management'),
   path('leave/delete/<int:pk>/', views.delete_leave, name='delete-leave'),

   path('approve-leave/<int:leave_id>/', views.approve_leave, name='approve-leave'),
   path('reject-leave/<int:leave_id>/', views.reject_leave, name='reject-leave'),

   path('payslip/pdf/<int:slip_id>/', views.generate_payslip_pdf, name='generate_payslip_pdf'),
   


    

]

