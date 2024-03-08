
from django.urls import path
from . import views

urlpatterns = [
    path('cookie',views.startApp),
    path('student',views.get_students, name='students'),
    path('address',views.get_address),
    path('createStudent', views.create_students, name='createStudent')

]
