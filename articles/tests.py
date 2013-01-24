"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from articles.models import *
from django.template import Context

class PublishingOutletTests(TestCase):
    fixtures = ['initial_data.yaml', 'test_data.yaml'] 
    class Request(object):
        build_absolute_uri="http://www.webaxis.com/article/1/"
    def setUp(self):
        self.fred=User.objects.get(username='fred')
        self.article=Article.objects.get(pk=1)
        self.request=self.Request()
        self.facebook_outlet=PublishingOutlet.objects.get(pk=2)
        self.wordpress_outlet=PublishingOutlet.objects.get(pk=4)
        
    def test_adding_facbook_outlet_to_user_and_getting_button_url(self):
        outlet=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.facebook_outlet)
        c=Context({'article':self.article, 'request':self.request})
        self.assertEqual(outlet.get_button_url(c), "http://facebook.com/sharer.php?u=http://www.webaxis.com/article/1/&amp;t=THETITLEGOESHERE")
        self.assertEqual(self.fred.publishing_outlets.all(),[outlet])
        
    def test_adding_wordpress_outlets_to_user_and_getting_button_url(self):
        outlet=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.wordpress_outlet)
        c=Context({'article':self.article, 'request':self.request})
        self.assertEqual(outlet.get_button_url(c), "")
        self.assertEqual(self.fred.publishing_outlets.all(),[outlet])
        
    def test_getting_list_of_outlets_for_user(self):
        outlet1=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.facebook_outlet)
        outlet2=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.wordpress_outlet)
        outlet3=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.wordpress_outlet)
        self.assertEqual(list(self.fred.publishing_outlets.all()),[outlet1, outlet2, outlet3])
    def fetch_the_module_for_an_outlet_and_run_action(self):
        outlet1=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.facebook_outlet)
