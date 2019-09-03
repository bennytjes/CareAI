from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('form/', include('complianceform.urls')),
]
