from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Admin, Machine, User
from django.utils import timezone

import json


# def index(request):
#     template = loader.get_template('laundry/index.html')
#     context = {
#         'machines': Machine.all_machine(),
#         'admins': Admin.all_admin()
#     }
#     return HttpResponse(template.render(context, request))

def control(request):
    template = loader.get_template('laundry/control.html')
    return HttpResponse(template.render({}, request))


def index(request):
    print(request)
    template = loader.get_template('laundry/index.html')
    return HttpResponse(template.render({}, request))


def laundry_js(request):
    template = loader.get_template('laundry/laundry.js')
    return HttpResponse(template.render({}, request))


def login(request):
    template = loader.get_template('laundry/login.html')
    return HttpResponse(template.render({}, request))


def machine(request):
    template = loader.get_template('laundry/machine.html')
    return HttpResponse(template.render({}, request))


def machinebusy_css(request):
    template = loader.get_template('laundry/machinebusy.css')
    return HttpResponse(template.render({}, request))


def machinebusy(request):
    template = loader.get_template('laundry/machinebusy.html')
    return HttpResponse(template.render({}, request))


def mystyle_css(request):
    template = loader.get_template('laundry/mystyle.css')
    return HttpResponse(template.render({}, request))


def timer_css(request):
    template = loader.get_template('laundry/timer.css')
    return HttpResponse(template.render({}, request))


def timer(request):
    template = loader.get_template('laundry/timer.html')
    return HttpResponse(template.render({}, request))


def UserForm(request):
    template = loader.get_template('laundry/UserForm.html')
    return HttpResponse(template.render({}, request))


def userformstyle_css(request):
    template = loader.get_template('laundry/userformstyle.css')
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
        print(err.args[0])
        return HttpResponse(json.dumps({"error": err.args[0]}))


def add_machine(request, admin, type, name, min_time, max_time, room):
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
        machines.append({"name": machine.name, "id": machine.id, "type": machine.type, "last_user": {"name": "N/A", "email": "N/A", "start_time": -1, "duration": -1} if len(last_user) == 1 or (
            last_user[3] + last_user[4] * 60 * 1000 < int(timezone.now().timestamp() * 1000)) else {"name": last_user[1], "email": last_user[2], "start_time": last_user[3], "duration": last_user[4]}})
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
        if len(m_info) == 1:
            return HttpResponse(json.dumps({"machine_name": m_info[0]}))
        else:
            return HttpResponse(json.dumps({"machine_name": m_info[0], "name": m_info[1], "email": m_info[2], "start_time": m_info[3], "duration": m_info[4]}))
    except AssertionError as err:
        return HttpResponse(json.dumps({"error": err.args[0]}))
