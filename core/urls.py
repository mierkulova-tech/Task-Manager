from django.contrib import admin
from django.urls import path, include
from tasks  import  views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('about/', views.about),
    path('posts/', include('posts.urls')),
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)