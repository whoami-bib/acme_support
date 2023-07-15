from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    DEPARTMENT_CHOICES = (
        ('1', 'Department 1'),
        ('2', 'Department 2'),
    )

    ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    department = models.CharField(max_length=1, choices=DEPARTMENT_CHOICES)
    role = models.CharField(max_length=10, choices=ROLES, default='user')

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    priority = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
