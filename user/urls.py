from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name = 'logout'),
    path('register/', views.register ,name='register'),
    path('change_password/',views.change_password, name='change_password'),
    path('profile/', views.profile, name =  'profile'),
    path('profile/edit/', views.profile_edit,name = 'profile_edit'),
    path('products/', views.products, name = 'products'),
    path('products/register/', views.products_register, name = 'products_register'),
    path('products/<int:product_id>',views.product_edit, name = 'product_edit'),
    ]