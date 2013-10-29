from vanilla.tests import BaseTestCase as VanillaBaseTestCase
from vanilla.tests import InstanceOf
from django.conf import settings
from django.test.client import Client
from articles.models import User

class BaseTestCase(VanillaBaseTestCase):
  def login(self, username='jared', password='t1bur0n'):
    response = self.c.post('/accounts/login/', {'username': username, 'password': password})
    # print "User.objects.all().count() = %s" % str(User.objects.all().count())
    self.assertEqual(response.status_code, 302)
  def setUp(self):
    settings.DEBUG = True
    self.c = Client()
    self.login()
    self.me = User.objects.get(pk=1)
  def assertMessages(self, response, expected):
    messages = [str(msg) for msg in response.context['messages']]
    for msg in messages: self.assertTrue(msg in expected, "context contains unexpected message: '%s'" % msg)
    for msg in expected: self.assertTrue(msg in messages, "context missing message: '%s'" % msg)
