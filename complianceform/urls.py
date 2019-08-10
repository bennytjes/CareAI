from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'complianceform'
urlpatterns = [
    path('<int:principle_id>/principlelist', views.principle_list, name= 'principle_list'),
    path('<int:principle_id>/complete', views.form_completed, name = 'form_completed'),
    path('form_changed', views.form_changed, name = 'form_changed'),
    path('view/<int:entry_id>', views.view_submissions, name = 'view_submission'),
    path('radar',views.radar, name = 'radar')
]