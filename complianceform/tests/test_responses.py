from django.test import SimpleTestCase
from django.urls import reverse, resolve
from complianceform.responses import getNumberRanking,getProductScores,getRankingScores


def test_get_number_ranking(self):
        url = reverse('complianceform:getNumberRanking',kwargs = {'group' : 'Other', 'audited': False })
        self.assertEquals(resolve(url).func,getNumberRanking)

def test_get_product_scores(self):
        url = reverse('complianceform:getProductScores',kwargs = {'group' : 'Other', 'audited': False })
        self.assertEquals(resolve(url).func,getProductScores)

def test_ranking_scores(self):
        url = reverse('complianceform:ranking_score',kwargs = {'group' : 'Other', 'audited': False })
        self.assertEquals(resolve(url).func,ranking_score)


