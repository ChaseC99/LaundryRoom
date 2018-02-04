from django.db import models
from django.utils import timezone
from datetime import datetime
import re
import pyqrcode
from pathlib import Path
email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
alphanumeric_re = re.compile(r"^[a-zA-Z0-9_.-]+$")


class Admin(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=1024)

    def __str__(self)->str:
        return "<" + str(self.id) + "> Admin: " + self.username

    @staticmethod
    def auth(username, password)->bool:
        return Admin.objects.filter(username=username.lower(), password=password).count() == 1

    @staticmethod
    def add_admin(username, password):
        assert type(username) is str and alphanumeric_re.match(
            username) is not None, "Username must be a non-empty string"
        assert type(password) is str and alphanumeric_re.match(
            password) is not None, "Password must be a non-empty string"
        assert Admin.objects.filter(
            username=username).count() == 0, "Admin already exists"
        Admin(username=username.lower(), password=password).save()

    def add_machine(self, m_type, name, min_time, max_time, room) -> "machine":
        assert type(m_type) is str and alphanumeric_re.match(
            m_type) is not None, "Type must be a non-empty string"
        assert type(name) is str and len(
            name) > 0, "Name must be a non-empty string"
        assert type(
            min_time) is int and min_time > 0, "Min_time must be a positive integer"
        assert type(
            max_time) is int and max_time > min_time, "Max_time must be greater than min_time"
        assert type(room) is str and alphanumeric_re.match(
            room) is not None, "Room must be a non-empty string"
        return self.machine_set.create(type=m_type, name=name,
                                       min_time=min_time, max_time=max_time, room=room)


class Machine(models.Model):
    type = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    min_time = models.IntegerField()
    max_time = models.IntegerField()
    room = models.CharField(max_length=64)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self)->str:
        return "<" + str(self.id) + "> " + self.type + ": '" + self.name + "' in '" + self.room + "'(" + self.admin.username + ")"

    @staticmethod
    def all_machine() -> {str: [(int, str)]}:
        return_data = {}
        for machine in Machine.objects.order_by():
            return_data.setdefault(machine.type, [])
            return_data[machine.type].append((machine.id, machine.name))
        return return_data

    def add_user(self, name, email, duration):
        assert type(name) is str and len(
            name) > 0, "Name must be a non-empty string"
        assert type(email) is str and email_re.match(
            email) is not None, "Invalid email"
        assert type(
            duration) is int and self.min_time <= duration <= self.max_time, "Duration is out of range"
        num_of_users = self.user_set.count()
        assert num_of_users == 0 or self.user_set.order_by(
            "start_time")[num_of_users - 1:num_of_users].get().end(), "This machine is in use"
        self.user_set.create(name=name, email=email,
                             start_time=timezone.now(), duration=duration)

    def machine_info(self) -> (str, int, int, str, str, int, int):
        num_of_users = self.user_set.count()
        if num_of_users <= 0:
            return (self.name, self.min_time, self.max_time)
        last_user = self.user_set.order_by(
            "start_time")[num_of_users - 1:num_of_users].get()
        return (self.name, self.min_time, self.max_time, last_user.name, last_user.email, last_user.get_start_timestamp(), last_user.duration)

    def gen_qr(self):
        url = pyqrcode.create(
            "http://169.234.81.18:8000/s/machine.html?id=" + str(self.id))
        url.png("../static/img/" +
                str(self.id) + ".png", scale=10)


class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=1024)
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    def __str__(self)->str:
        return "<" + str(self.id) + "> " + self.start_time.isoformat(" ") + " / " + self.name + "(" + str(self.duration) + "mins)"

    def get_start_timestamp(self)->int:
        return int(self.start_time.timestamp() * 1000)

    def end(self)->bool:
        return self.get_start_timestamp() + self.duration * 60 * 1000 < int(timezone.now().timestamp() * 1000)
