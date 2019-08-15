from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'complianceform'
urlpatterns = [
    path('<int:principle_id>/principlelist', views.principle_list, name= 'principle_list'),
    path('<int:principle_id>/complete', views.form_completed, name = 'form_completed'),
    path('form_changed', views.form_changed, name = 'form_changed'),
    path('view/<int:entry_id>', views.view_submissions, name = 'view_submission'),
    path('analytics', views.analytics, name = 'analytics'),
    path('radar',views.radar, name = 'radar'),
    path('completeness_ranking',views.completeness_ranking, name = 'completeness_ranking'),
    path('number_ranking',views.number_ranking, name = 'number_ranking'),
    path('radar_analytics',views.radar_analytics, name = 'radar_analytics'),
    path('getProductScores', views.getProductScores, name = 'getProductScores'),
    path('ranking_score/<str:group>', views.rankingScore, name = 'ranking_score'),
]