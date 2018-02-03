from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /machine/5/
    path('machine/<int:machine_id>/', views.machine, name='machine'),
    # ex: /machine/5/register/
    path('machine/<int:machine_id>/register/', views.register, name='register'),
    # ex: /machine/5/timer/
    path('machine/<int:machine_id>/timer/', views.timer, name='timer'),
]
