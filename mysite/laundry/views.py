from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Admin, Machine, User
from django.utils import timezone

import json


def index(request):
    template = loader.get_template('laundry/index.html')
    context = {
        'machines': Machine.all_machine(),
        'admins': Admin.all_admin()
    }
    return HttpResponse(template.render(context, request))


def machine(request, machine_id):
    return HttpResponse("You're looking at machine %s." % machine_id)


def timer(request, machine_id):
    return HttpResponse("You're looking at timer of machine %s." % machine_id)

# API


def all_machine(request, room):
    machines = [{"name": machine.name, "id": machine.id, "type": machine.type}
                for machine in Machine.objects.filter(room=room).order_by("name")]
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
        return HttpResponse(json.dumps({"machine_name": m_info[0], "name": m_info[1], "email": m_info[2], "start_time": m_info[3], "duration": m_info[4]}))
    except AssertionError as err:
        return HttpResponse(json.dumps({"error": err.args[0]}))
