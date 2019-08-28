from django.test import SimpleTestCase
from django.urls import reverse, resolve
from complianceform.views import *



class Test_ComplianceForm_Urls(SimpleTestCase):
    def test_principlelist(self):
        url = reverse('complianceform:principle_list',kwargs = {'principle_id' :1, 'product_id': 12})
        self.assertEquals(resolve(url).func,principle_list)

    def test_form_completed(self):
        url = reverse('complianceform:form_completed',kwargs = {'principle_id' :1})
        self.assertEquals(resolve(url).func,form_completed)

    def test_form_changed(self):
        url = reverse('complianceform:form_changed')
        self.assertEquals(resolve(url).func,form_changed)

    def test_JotFormID(self):
        url = reverse('complianceform:JotFormID')
        self.assertEquals(resolve(url).func,JotFormID)

    def test_view_submissions(self):
        url = reverse('complianceform:view_submissions',kwargs = {'product_id' :12, 'entry_id': 0})
        self.assertEquals(resolve(url).func,view_submissions)
    
    def test_analytics(self):
        url = reverse('complianceform:analytics')
        self.assertEquals(resolve(url).func,analytics)

    def test_radar(self):
        url = reverse('complianceform:completeness_ranking')
        self.assertEquals(resolve(url).func,completeness_ranking)

    def test_number_ranking(self):
        url = reverse('complianceform:number_ranking')
        self.assertEquals(resolve(url).func,number_ranking)
    
    def test_radar_analytics(self):
        url = reverse('complianceform:radar_analytics')
        self.assertEquals(resolve(url).func,radar_analytics)

