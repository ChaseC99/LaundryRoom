from django.urls import path

from . import views

urlpatterns = [
    path('control', views.control, name='control'),
    path('login', views.login, name='login'),
    # API
    # ex: /api/auth/admin/5m3ofp350...
    path('api/auth/<str:username>/<str:password>/', views.auth, name='auth'),
    # ex: /api/register/admin/5m3ofp350...
    path('api/register/<str:username>/<str:password>/',
         views.register, name='register'),
    # ex: /api/add_machine/washer/washer#1/30/60/laundryroom
    path('api/add_machine/<str:type>/<str:name>/<int:min_time>/<int:max_time>/<str:room>/',
         views.add_machine, name='add_machine'),
    # ex: /api/all_machine/nieblaLaundryRoom
    path('api/all_machine/<str:room>/', views.all_machine, name='all_machine'),
    # ex: /api/new_user/john/john@test.com/45
    path('api/new_user/<int:machine_id>/<str:name>/<str:email>/<int:duration>',
         views.new_user, name='new_user'),
    # ex: /api/machine_info/1
    path('api/machine_info/<int:machine_id>',
         views.machine_info, name='machine_info'),
]
