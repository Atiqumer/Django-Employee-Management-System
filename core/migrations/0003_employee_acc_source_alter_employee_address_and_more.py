# Generated by Django 5.1.3 on 2025-06-03 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_employee_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="acc_source",
            field=models.CharField(default="00", max_length=15),
        ),
        migrations.AlterField(
            model_name="employee",
            name="Address",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="employee",
            name="account",
            field=models.CharField(max_length=25),
        ),
    ]
