from django.urls import path
from posts  import  views

app_name = 'posts'
urlpatterns = [
    path('', views.posts_list, name="list"),
    path('<slug:slug>/', views.post_page, name="page"),
]