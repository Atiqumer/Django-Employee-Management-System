# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee
from datetime import date

@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        if not hasattr(instance, 'employee'):
            Employee.objects.create(
            user=instance,
            name=instance.get_full_name() or instance.username,
            join_date=date.today() 
        )
