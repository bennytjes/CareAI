from django.test import SimpleTestCase
from django.urls import reverse, resolve
from complianceform.views import *


class Test_ComplianceForm_Urls(SimpleTestCase):
    def test_principlelist(self):
        url = reverse('complianceform:principle_list',kwargs = {'principle_id' :1, 'product_id': 12})
        self.assertEquals(resolve(url).func,principle_list)


# urlpatterns = [
#     path('principlelist/<int:principle_id>/<int:product_id>', views.principle_list, name= 'principle_list'),
#     path('<int:principle_id>/complete', views.form_completed, name = 'form_completed'),
#     path('form_changed', views.form_changed, name = 'form_changed'),
#     path('view/<int:product_id>/<int:entry_id>/', views.view_submissions, name = 'view_submission'),
#     path('analytics', views.analytics, name = 'analytics'),
#     path('radar',views.radar, name = 'radar'),
#     path('completeness_ranking',views.completeness_ranking, name = 'completeness_ranking'),
#     path('number_ranking',views.number_ranking, name = 'number_ranking'),
#     path('getNumberRanking/<str:group>/<str:audited>',responses.getNumberRanking, name = 'getNumberRanking'),
#     path('radar_analytics',views.radar_analytics, name = 'radar_analytics'),
#     path('getProductScores/<str:group>/<str:audited>', responses.getProductScores, name = 'getProductScores'),
#     path('ranking_score/<str:group>/<str:audited>', responses.getRankingScores, name = 'ranking_score'),
# ]