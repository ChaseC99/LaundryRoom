from django.db import models


class Admin(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=1024)


class Machine(models.Model):
    type = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    min_time = models.IntegerField()
    max_time = models.IntegerField()
    room = models.CharField(max_length=64)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)


class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=1024)
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
