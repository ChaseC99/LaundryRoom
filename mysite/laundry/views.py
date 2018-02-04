from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Admin, Machine, User
from django.utils import timezone
from datetime import datetime

import json


# def index(request):
#     template = loader.get_template('laundry/index.html')
#     context = {
#         'machines': Machine.all_machine(),
#         'admins': Admin.all_admin()
#     }
#     return HttpResponse(template.render(context, request))
def admin_auth(request):
    if Admin.auth(request.COOKIES.get("laundry_admin_username", ""),
                  request.COOKIES.get("laundry_admin_password", "")) == False:
        raise Http404("Access denied")


def control(request):
    admin_auth(request)
    template = loader.get_template('laundry/control.html')
    machines = Admin.objects.get(
        username=request.COOKIES["laundry_admin_username"]).machine_set.order_by()
    machine_list = []
    for machine in machines:
        data = {}
        data["id"] = str(machine.id)
        data["type"] = machine.type[0].upper() + machine.type[1:].lower()
        data["name"] = machine.name
        data["duration"] = str(machine.min_time) + \
            " - " + str(machine.max_time)
        data["room"] = machine.room
        num_of_users = machine.user_set.count()
        if num_of_users <= 0:
            data["status"] = "Free"
        else:
            last_user = machine.user_set.order_by(
                "start_time")[num_of_users - 1:num_of_users].get()
            if last_user.end():
                data["status"] = "Free"
            else:
                data["status"] = last_user.name + datetime.fromtimestamp(
                    (last_user.get_start_timestamp() + last_user.duration * 60 * 1000) / 1000).strftime(" (%x %H:%M)")
        machine_list.append(data)
    context = {
        "machines": machine_list
    }
    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('laundry/login.html')
    return HttpResponse(template.render({}, request))


# API


def auth(request, username, password):
    try:
        return HttpResponse(json.dumps({"valid": Admin.auth(username, password)}))
    except AssertionError as err:
        return HttpResponse(json.dumps({"error": err.args[0]}))


def register(request, username, password):
    try:
        Admin.add_admin(username, password)
        return HttpResponse(json.dumps({}))
    except AssertionError as err:
        return HttpResponse(json.dumps({"error": err.args[0]}))


def add_machine(request, type, name, min_time, max_time, room):
    admin_auth(request)
    admin = request.COOKIES["laundry_admin_username"]
    a = Admin.objects.get(username=admin)
    try:
        a.add_machine(type, name, min_time, max_time, room).gen_qr()
        return HttpResponse(json.dumps({}))
    except AssertionError as err:
        return HttpResponse(json.dumps({"error": err.args[0]}))


def all_machine(request, room):
    machines = []
    for machine in Machine.objects.filter(room=room).order_by("name"):
        last_user = machine.machine_info()
        machines.append({"name": machine.name, "id": machine.id, "type": machine.type, "last_user": {"name": "N/A", "email": "N/A", "start_time": -1, "duration": -1} if len(last_user) == 3 or (
            last_user[5] + last_user[6] * 60 * 1000 < int(timezone.now().timestamp() * 1000)) else {"name": last_user[3], "email": last_user[4], "start_time": last_user[5], "duration": last_user[6]}})
    return HttpResponse(json.dumps({"machines": machines}))


def new_user(request, machine_id, name, email, duration):
    m = Machine.objects.get(id=machine_id)
    try:
        m.add_user(name=name, email=email, duration=duration)
        return HttpResponse(json.dumps({}))
    except AssertionError as err:
        return HttpResponse(json.dumps({"error": err.args[0]}))


def machine_info(request, machine_id):
    try:
        m_info = Machine.objects.get(id=machine_id).machine_info()
        if len(m_info) == 3:
            return HttpResponse(json.dumps({"machine_name": m_info[0], "min_time": m_info[1], "max_time": m_info[2]}))
        else:
            return HttpResponse(json.dumps({"machine_name": m_info[0], "min_time": m_info[1], "max_time": m_info[2], "name": m_info[3], "email": m_info[4], "start_time": m_info[5], "duration": m_info[6]}))
    except AssertionError as err:
        return HttpResponse(json.dumps({"error": err.args[0]}))
