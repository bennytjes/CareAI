from django.test import TestCase,Client
from django.urls import reverse
from complianceform.models import *
from django.contrib.auth.models import User
from user.models import UserDetails

class Test_ComplianceForm_Views(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='djangodjango')
        self.test_user.save()
        self.test_product = Products(user_id = self.test_user,product_name = 'testproduct',category='Other',deploy_point = 'Other',description = 'test')
        self.test_product.save()
        self.client.login(username='testuser',password = 'djangodjango')
        self.test_userdetail= UserDetails(user_id = self.test_user,username = 'testuser',is_supplier=False)
        self.test_userdetail.save()
        session = self.client.session
        session['product_id'] = self.test_product.pk
        session.save()
        self.test_form_id = JotFormIDs(principle=11,jotform_id = '0000000000')
        self.test_form_id.save()

    def test_principle_list_GET(self):
        response = self.client.get(reverse('complianceform:principle_list',kwargs = {'principle_id' :self.test_form_id.principle, 'product_id': self.test_product.pk}))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'embeded_form.html')

    def test_form_completed_GET(self):
        response = self.client.get(reverse('complianceform:form_completed',kwargs = {'principle_id' :self.test_form_id.principle,}))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'form_completed.html')
    
    def test_form_changed_GET(self):
        response = self.client.get(reverse('complianceform:form_changed'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'form_changed.html')

    def test_view_submissions_GET(self):
        response = self.client.get(reverse('complianceform:view_submissions',kwargs = {'entry_id':0,'product_id':self.test_product.pk}))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'view_submissions.html')

    def test_radar_GET(self):
        response = self.client.get(reverse('complianceform:radar'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'radar.html')

    def test_radar_analytics_GET(self):
        response = self.client.get(reverse('complianceform:radar_analytics'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'radar_analytics.html')

    def test_completeness_ranking_GET(self):
        response = self.client.get(reverse('complianceform:completeness_ranking'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'completeness_ranking.html')

    def test_number_ranking_GET(self):
        response = self.client.get(reverse('complianceform:number_ranking'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'number_ranking.html')

    def test_analytics_GET(self):
        response = self.client.get(reverse('complianceform:analytics'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'analytics.html')

    def test_JotFormID_GET(self):
        response = self.client.get(reverse('complianceform:JotFormID'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'JotFormID.html')

    def test_JotformID_POST(self):
        response = self.client.post('/form/JotFormID',{})
        self.assertEquals(response.status_code,200)