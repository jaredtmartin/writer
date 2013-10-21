"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class ElementTest(TestCase):
    def test_header(self):
        e = Element.objects.create(klass=Element.HEADER, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
    def test_textbox(self):
        e = Element.objects.create(klass=Element.TEXTBOX, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
    def test_textbox(self):
        e = Element.objects.create(klass=Element.TEXTAREA, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
    def test_textbox(self):
        e = Element.objects.create(klass=Element.DROPDOWN, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
    def test_textbox(self):
        e = Element.objects.create(klass=Element.RADIO, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
    def test_textbox(self):
        e = Element.objects.create(klass=Element.CHECKBOX, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
    def test_textbox(self):
        e = Element.objects.create(klass=Element.FILEUPLOAD, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
    def test_textbox(self):
        e = Element.objects.create(klass=Element.SUBMIT, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
    def test_textbox(self):
        e = Element.objects.create(klass=Element.PASSWORD, name="Name")
        self.assertEqual(e.unicode(), u'<h1>Name</h1>')
        
