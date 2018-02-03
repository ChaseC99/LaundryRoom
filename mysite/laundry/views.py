from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Admin, Machine, User


# def index(request):
#     return HttpResponse("Hello, world. You're at the laundry index.")


def index(request):
    admin_list = Admin.objects.order_by()
    template = loader.get_template('laundry/index.html')
    context = {
        'admin_list': admin_list,
    }
    return HttpResponse(template.render(context, request))


def machine(request, machine_id):
    return HttpResponse("You're looking at machine %s." % machine_id)


def register(request, machine_id):
    response = "You're looking at the register paage of machine %s."
    return HttpResponse(response % machine_id)


def timer(request, machine_id):
    return HttpResponse("You're looking at timer of machine %s." % machine_id)
