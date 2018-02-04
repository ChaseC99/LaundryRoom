from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /machine/5/
    path('machine/<int:machine_id>/', views.machine, name='machine'),
    # ex: /machine/5/timer/
    path('machine/<int:machine_id>/timer/', views.timer, name='timer'),
    # API
    # ex: /api/all_machine/nieblaLaundryRoom
    path('api/all_machine/<str:room>/', views.all_machine, name='all_machine'),
    # ex: /api/new_user/john/john@test.com/45
    path('api/new_user/<int:machine_id>/<str:name>/<str:email>/<int:duration>',
         views.new_user, name='new_user'),
    # ex: /api/machine_info/1
    path('api/machine_info/<int:machine_id>',
         views.machine_info, name='machine_info'),
]
