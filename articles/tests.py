"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from articles.models import *
from django.template import Context

FACEBOOK_BUTTON=u"""<div id="fb-root"></div>\n<script>\n  // Additional JS functions here\n  function login() {\n    //Use this to prompt people to log into Facebook\n        FB.login(function(response) {\n            if (response.authResponse) {\n                // connected\n            } else {\n                // cancelled\n            }\n        }, {scope: \'publish_stream\'});\n    }\n    function testAPI() {\n        console.log(\'Welcome!  Fetching your information.... \');\n        FB.api(\'/me\', function(response) {\n            console.log(\'Good to see you, \' + response.name + \'.\');\n        });\n    }\n    \n  window.fbAsyncInit = function() {\n    FB.init({\n      appId      : \'519129288106424\', // App ID\n      channelUrl : \'/static/js/channel.html\', // Channel File\n      status     : true, // check login status\n      cookie     : true, // enable cookies to allow the server to access the session\n      xfbml      : true  // parse XFBML\n    });\n\n    FB.getLoginStatus(function(response) {\n      if (response.status === \'connected\') {\n        // connected\n        testAPI();\n      } else if (response.status === \'not_authorized\') {\n        // not_authorized\n        login();\n      } else {\n        // not_logged_in\n        login();\n      }\n     });\n\n     \n  };\n\n  // Load the SDK Asynchronously\n  (function(d){\n     var js, id = \'facebook-jssdk\', ref = d.getElementsByTagName(\'script\')[0];\n     if (d.getElementById(id)) {return;}\n     js = d.createElement(\'script\'); js.id = id; js.async = true;\n     js.src = "//connect.facebook.net/en_US/all.js";\n     ref.parentNode.insertBefore(js, ref);\n   }(document));\n</script>\n\n<script>\n    function post_on_facebook(title,body){\n        FB.api(\'/me/feed\', \'post\', {message:body,name:title},\n            function(response) {\n                if (!response || response.error) {\n                    alert(\'Error occured\');\n                } else {\n                    alert(\'Post ID: \' + response.id);\n                }\n        });\n    }\n</script>\n<a onclick="post_on_facebook($(\'#id_title\').val(), $(\'#id_body\'));return false;">Post to Facebook</a>\n"""
TWITTER_BUTTON=u'<a href="http://twitter.com/home?status=%3Cp%3ECan%20%3Cspan%20style%3D%22background-color%3A%20%23ffff00%3B%22%3Eyou%3C/span%3E%20hear%20the%20words%20%3Cstrong%3Ecoming%3C/strong%3E%20out%20of%20my%20%3Cspan%20style%3D%22color%3A%20%23ff0000%3B%22%3Emouth%3C/span%3E%3F%26nbsp%3B%20I%20really%20%3Cspan%20style%3D%22text-decoration%3A%20underline%3B%22%3E%3Cstrong%3Ehope%3C/strong%3E%3C/span%3E%20this%20works%21s%3C/p%3E%0D%0A%3Cul%3E%0D%0A%3Cli%3EDog%3C/li%3E%0D%0A%3Cli%3ECat%3C/li%3E%0D%0A%3Cli%3EBird%3C/li%3E%0D%0A%3C/ul%3E%0D%0A%3Cp%3ESome%20%3Cspan%20style%3D%22font-size%3A%20large%3B%22%3Emore%3C/span%3E%20stuff%20down%20here.%3C/p%3E%20Jumper">Twitter</a>'
class PublishingOutletTests(TestCase):
    fixtures = ['initial_data.yaml', 'test_data.yaml'] 
    class Request(object):
        build_absolute_uri="http://www.webaxis.com/article/1/"
    def setUp(self):
        self.fred=User.objects.get(username='fred')
        self.article=Article.objects.get(pk=1)
        self.request=self.Request()
        self.facebook_outlet=PublishingOutlet.objects.get(pk=1)
        self.wordpress_outlet=PublishingOutlet.objects.get(pk=3)
        
    def test_adding_facbook_outlet_to_user_and_getting_button_url(self):
        outlet=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.facebook_outlet)
        c=Context({'article':self.article, 'request':self.request})
        self.assertEqual(outlet.get_button_url(context=c), FACEBOOK_BUTTON)
        self.assertEqual(self.fred.publishing_outlets.all(),[outlet])
        
    def test_adding_wordpress_outlets_to_user_and_getting_button_url(self):
        outlet=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.wordpress_outlet)
        c=Context({'article':self.article, 'request':self.request})
        self.assertEqual(outlet.get_button_url(context=c), TWITTER_BUTTON)
        self.assertEqual(self.fred.publishing_outlets.all(),[outlet])
        
    def test_getting_list_of_outlets_for_user(self):
        outlet1=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.facebook_outlet)
        outlet2=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.wordpress_outlet)
        outlet3=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.wordpress_outlet)
        self.assertEqual(list(self.fred.publishing_outlets.all()),[outlet1, outlet2, outlet3])
    def fetch_the_module_for_an_outlet_and_run_action(self):
        outlet1=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.facebook_outlet)
        
class ArticleTests(TestCase):
    fixtures = ['initial_data.yaml', 'test_data.yaml'] 
    def setUp(self):
        self.writer= User.objects.get(username='writer')
        self.requester= User.objects.get(username='requester')
        self.fred=User.objects.get(username='fred')
        self.blog = ArticleType.objects.get(name='Blog')
        
    def test_available_actions_with_new_article_and_user_that_is_not_owner(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        self.assertEqual(article.get_available_actions(self.fred), ['claim'])
        
    def test_available_actions_with_new_article_and_owner(self):    
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        self.assertEqual(article.get_available_actions(self.requester), ['assign'])
        
    def test_available_actions_with_the_assigned_writer_when_he_can_submit(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='G', user=self.requester, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.writer), ['submit','release'])
        
    def test_available_actions_with_the_claimed_writer_when_he_can_submit(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='C', user=self.writer, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.writer), ['submit','release'])

    def test_available_actions_with_the_assigned_writer_after_he_submitted(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='S', user=self.writer, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.writer), [])
        
    def test_available_actions_with_the_owner_when_hes_waiting_on_the_writer(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='G', user=self.requester, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.requester), ['release'])
        
    def test_available_actions_with_the_owner_after_writer_has_submitted(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='S', user=self.writer, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.requester), ['approve','reject'])
        
    def test_available_actions_with_other_user_after_article_has_been_assigned_to_someone_else(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='G', user=self.requester, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.fred), [])
        
    def test_available_actions_with_other_user_after_article_has_been_submitted_by_someone_else(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='S', user=self.writer, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.fred), [])
        
    def test_available_actions_with_the_owner_after_he_has_published(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='P', user=self.requester, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.requester), [])
        
    def test_available_actions_with_the_writer_after_owner_has_published(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='P', user=self.requester, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.writer), [])
        
    def test_available_actions_with_the_other_user_after_owner_has_published(self):
        article=Article.objects.create(owner=self.requester, article_type=self.blog)
        action=ArticleAction.objects.create(code='P', user=self.requester, author=self.writer)
        article.add_action(action)
        self.assertEqual(article.get_available_actions(self.fred), [])

class StatusFilterTests(TestCase):
    def test_getting_choices_when_there_is_a_article_that_has_no_actions(self):
        pass
        
