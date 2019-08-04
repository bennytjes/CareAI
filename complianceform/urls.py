from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'complianceform'
urlpatterns = [
    path('<int:product_id>/<int:principle_id>/principlelist', views.principle_list, name= 'principle_list'),
    path('<int:product_id>/<int:principle_id>/complete', views.form_completed, name = 'form_completed'),
    path('form_changed', views.form_changed, name = 'form_changed'),
    path('showpost',views.showpost, name = 'showpost')
]