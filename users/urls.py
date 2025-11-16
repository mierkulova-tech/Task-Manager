from django.urls import path
from users  import  views

app_name = 'users'

urlpatterns = [
    path('', views.users_redirect_to_register, name='users_home'),
    path('register/', views.register_view, name="register"),
]