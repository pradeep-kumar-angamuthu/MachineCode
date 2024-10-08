# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('SUPERADMIN', 'Super Admin'),
        ('MANAGER', 'Manager'),
        ('SUPERVISOR', 'Supervisor'),
        ('OPERATOR', 'Operator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OPERATOR')

    def __str__(self):
        return self.username

# models.py
class Machine(models.Model):
    machine_data_id = models.AutoField(primary_key=True)
    machine_id = models.IntegerField(default=1)
    axis_id = models.IntegerField(null=True)  # Change to IntegerField to match your table schema
    tool_offset = models.FloatField()  # Real type in SQLite corresponds to FloatField in Django
    feedrate = models.IntegerField()  # Matches INTEGER in SQLite
    tool_in_use = models.IntegerField(null=True)  # You can use BooleanField for true/false (0/1)
    timestamp = models.DateTimeField(auto_now_add=True)  # Use auto_now_add for default current timestamp

    class Meta:
        db_table = 'machine_data'  # Ensure this matches your SQLite table name

    def __str__(self):
        return str(self.machine_id)


