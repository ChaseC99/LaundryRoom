from django.db import models


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=1024)


class Machine(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    min_time = models.IntegerField()
    max_time = models.IntegerField()
    room = models.CharField(max_length=64)
    admin_id = models.IntegerField()
    # admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    last_user_id = models.IntegerField()


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    machine_id = models.IntegerField()
    # machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
