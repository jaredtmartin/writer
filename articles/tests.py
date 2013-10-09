"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, LiveServerTestCase
from django.test.client import Client as TestClient
from articles.models import Article, User, PublishingOutlet, PublishingOutletConfiguration, ArticleType, ArticleAction
from django.template import Context
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
import os   
import time
# from selenium.webdriver.firefox.webdriver import WebDriver

class MyFirefoxWebDriver(webdriver.Firefox):
    def get_element(self, text):
        return self.find_element_by_xpath("//*[.='%s']" % text)
    def get_link(self, text):
        return self.find_element_by_xpath('//a[contains(%s)' % text)
    def get_button(self, text):
        return self.find_element_by_css_selector('button:contains("%s")' % text)
    def get_body(self):
        return self.find_element_by_tag_name('body')
    def see_text_on_page(test, text):
        test.assertIn(test, text, self.get_body().text)
class BaseFunctionalTest(LiveServerTestCase):
    fixtures = ['initial_data.yaml', 'test_data.yaml']
    auto_login = False
    def setUp(self):
        self.browser = MyFirefoxWebDriver()
        self.browser.maximize_window()
        self.browser.implicitly_wait(5)
        if self.auto_login: self.login()
        # browser.implicitly_wait(10)
        # self.wait = WebDriverWait(self.browser, 10)
    def tearDown(self):
        self.browser.quit()
    # def wait_for_jquery(self):
    #     self.wait.until(self.browser.execute_script('return jQuery.active == 0'))
    def assert_see_on_page(self, text):
        self.assertIn(text, self.browser.get_body().text)
    def login(self):
        self.browser.get(self.live_server_url+'/accounts/login/')
        # He fills in his username and password and hits return
        self.browser.find_element_by_name('username').send_keys('requester')
        password_field=self.browser.find_element_by_name('password')
        password_field.send_keys('pass')
        password_field.send_keys(Keys.RETURN)
        # He sees the friendly welcome message in the top right corner with his name.
        body = self.browser.find_element_by_tag_name('body')
        self.browser.save_screenshot('screenie.png')
        self.assertIn('Hi Joe Requester!', body.text)

class CreateArticles(BaseFunctionalTest):
    auto_login = True
    def setUp(self):
        super(CreateArticles, self).setUp()
        self.browser.get(self.live_server_url)
        self.assert_see_on_page('Available Articles')
        self.browser.find_elements_by_link_text('NEW ARTICLE')[0].click()
    def test_bare_minimum(self):
        self.browser.find_elements_by_id("save-button")[0].click()
        self.browser.save_screenshot('screenie.png')
    def test_can_create_a_simple_set_of_articles(self):

        # Click on Article Type
        self.browser.find_elements_by_id("select-label-article_type")[0].click()
        # Select Simple Articles    
        self.browser.find_elements_by_link_text("Simple Articles")[0].click()
        

        # Sees the project field and decides to start a new one:
        # So he clicks on the plus sign next to project
        self.browser.find_elements_by_id("project-button")[0].click()
        # He sees a modal appear
        self.assert_see_on_page("Create a New Project")
        # He types in "Big Project" in the project name field
        self.browser.find_elements_by_id("project-name-input")[0].send_keys("Big Project")
        # He clicks "Create" and sees "Project: Big Project" in the box
        self.browser.find_elements_by_link_text("Create")[0].click()
        self.assert_see_on_page("Project: Big Project")
        # Sees the category field and decides to start a new category:
        # So he clicks on the plus sign next to category
        self.browser.find_elements_by_id("category-button")[0].click()
        # He sees a modal appear
        self.assert_see_on_page("Create a New Category")
        # He types in "Special" in the project name field
        i=self.browser.find_elements_by_id("category-name-input")[0].send_keys("Special")
        # He clicks "Create" and sees "Category: Special" in the box
        self.browser.find_elements_by_link_text("Create")[0].click()
        self.assert_see_on_page("Category: Special")
        # He Sees the priority option and sets it to low priority
        self.browser.find_elements_by_id("priority-button")[0].click()
        self.browser.find_elements_by_link_text("Low Priority")[0].click()
        # and sees the value has been accepted
        self.assert_see_on_page("Priority: Low Priority")
        #  he sees the field for number of articles and types "3"
        self.browser.find_elements_by_name("number_of_articles")[0].send_keys("3")
        # He then adds two keywords
        self.browser.find_elements_by_name("keyword_set-0-keyword")[0].send_keys("Atlanta Plumber")
        self.browser.find_elements_by_name("keyword_set-0-url")[0].send_keys("www.google.com")
        self.browser.find_elements_by_name("keyword_set-0-times")[0].send_keys("2")
        self.browser.find_elements_by_id("new-keyword-button")[0].click()
        self.browser.find_elements_by_name("keyword_set-1-keyword")[0].send_keys("Florida Orange")
        self.browser.find_elements_by_name("keyword_set-1-url")[0].send_keys("www.yahoo.com")
        # # Fill Article Notes with "Be sure to use good grammar."
        self.browser.find_elements_by_name("article_notes")[0].send_keys("Be sure to use good grammar.")
        # # Fill Review Notes with "Make sure they used good grammar"
        self.browser.find_elements_by_name("review_notes")[0].send_keys("Be sure to use good grammar.")
        self.browser.find_elements_by_id("save-button")[0].click()
    def test_writing_an_article(self):
        # John opens his browser and types www.writeraxis.com
        self.browser.get(self.live_server_url)
        # He sees his 3 articles there
        new_article_links = self.browser.find_elements_by_link_text("Atlanta Plumber")
        print "new_article_links = %s" % str(new_article_links)
        self.browser.save_screenshot('screenie.png')
        self.assertEquals(len(new_article_links), 5)
        new_article_links[0].click()
    def test_creating_projects(self):
        pass
    def test_creating_articles_without_notes(self):
        pass
    # TODO Test making an article with a Project
class LoginTest(BaseFunctionalTest):
    def test_can_login(self):
        # John opens his browser and types www.writeraxis.com
        # He is greeted and gets the articles list
        # body = self.browser.find_element_by_tag_name('body')
        # # self.assertIn('Welcome', body.text)
        # # He sees a link to 'add' a new poll, so he clicks it
        # login_link = self.browser.find_element_by_link_text('Log in')
        # login_link.click()

        # He gets redirected to the login screen

        self.browser.get(self.live_server_url+"/accounts/login")
        self.browser.maximize_window()
        # He fills in his username and password and hits return
        self.browser.find_element_by_name('username').send_keys('requester')
        password_field=self.browser.find_element_by_name('password')
        password_field.send_keys('pass')
        password_field.send_keys(Keys.RETURN)
        # self.browser.find_element_by_id('login-submit').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Hi Joe Requester!', body.text)
    # def test_with_bad_username(self):
    #     self.fail('Finish this test')
    # def test_with_bad_password(self):
    #     self.fail('Finish this test')

class ActionWorkflowTest(TestCase):
    fixtures = ['initial_data.yaml', 'test_data.yaml']
    def setUp(self):
        self.testclient = TestClient()
        response = self.testclient.post('/accounts/login/', {'username': 'requester', 'password': 'pass'})
        self.fred=User.objects.get(username='fred')
        self.writer= User.objects.get(username='writer')
        self.requester= User.objects.get(username='requester')
        self.article1 = Article.objects.get(pk=1)
        self.article2 = Article.objects.get(pk=2)
    def test_make_available(self):
        self.assertTrue(True)
        response = self.client.get(reverse('make_available_to_writer'))
        


# Keywords:
# Fill keyword with "Austin Plumber"
# Fill URL with "www.austinplumber.com"
# Fill Frequency with "2"
# Click on add a keyword
# Fill keyword with "qualities"
# Fill URL with "www.austinplumber.com/qualities/"
# Fill Frequency with "1"
# Click on "Save and Add Another"
# (This will create another article in the same project)
# Fill Description with "Another simple article"
# Set the Due Date to two Weeks from now  
# Set number of Articles to 20
# Fill Article Notes with "Be sure to use legal terms."
# Fill Review Notes with "Make sure they used legal terms"
# Fill Tags with "Medium, Legal"
# Keywords:
# Fill keyword with "Austin Lawyer"
# Fill URL with "www.austinlaw.com"
# Fill Frequency with "2"
# (We'll leave this article with only one keyword although we could add more)
# Click on Save Article
# Go to Articles list and make sure they are all displayed

# Create a Rewrite:
#     Click on New Article
#     Select "Big Project"
#     (Here we're using an existing project that has 2 simple articles in it)
#     Click on Article Type
#     Select Rewrite
#     Fill Name with "Fred's"
#     Fill Description with "Rewrites of Fred's Articles"
#     Set the Due Date to Next Week
#     Set number of Articles to 50
#     Fill Article Notes with "Be sure it's unique."
#     Fill Review Notes with "Make sure they made it unique"
#     Fill Tags with "Rewrite, Fred"
#     Copy and Paste Original into field labeled "Original Article"
#     Keywords:
#         Fill keyword with "Austin Lawyer"
#         Fill URL with "www.austinlaw.com"
#         Fill Frequency with "2"
#         (We'll leave this article with only one keyword although we could add more)
#     Click Save Article
# UAW Article:
#     Click on New Article
#     Click on Article Type
#     Select UAW Article Set
#     Click on New Project
#     (New Project Dialog Appears)
#     Type "Green Project"
#     Click on Create Project
#     (New Project Dialog Disappears and the name of the project appears in the form)
#     Fill Description with "A few UAW Articles for the green company"
#     Set the Due Date to Next Week
#     Set Number of Article Sets to 7
#     Fill Article Notes with "Don't run with sizzors."
#     Fill Review Notes with "Check Spelling"
#     Fill Tags with "Green, UAW"
#     Keywords:
#         Fill keyword with "Green Oil"
#         Fill URL with "www.exxonvaldez.com"
#         Fill Frequency with "1"
#     (We'll leave this article with only one keyword although we could add more)
# Now, Go back and make sure all of the Articles were created correctly

    






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
    # def fetch_the_module_for_an_outlet_and_run_action(self):
    #     outlet1=PublishingOutletConfiguration.objects.create(user=self.fred, outlet=self.facebook_outlet)
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
        
class PublishingOutletConfigurationTests(TestCase):
    fixtures = ['initial_data.yaml', 'test_data.yaml']
    def setUp(self):
        self.facebook= PublishingOutlet.objects.get(title='Facebook')
        self.fred=User.objects.get(username='fred')
        self.writer=User.objects.get(username='fred')
        self.fred=User.objects.get(username='fred')
    def test_saving_and_retrieving_data_from_a_configuration(self):
        poc=PublishingOutletConfiguration.objects.create(outlet=self.facebook, user=self.fred)
        poc.data={'cat':'pablito', 'username':'Jared', 'wins':123}
        self.assertEqual(poc.get_setting('cat'), 'pablito')
        poc.save()
        poc2=PublishingOutletConfiguration.objects.get()
        self.assertEqual(poc2.get_setting('wins'), 123)

class UserPropertiesTests(TestCase):
    fixtures = ['initial_data.yaml', 'test_data.yaml']
    def setUp(self):
        self.fred=User.objects.get(username='fred')
        self.writer= User.objects.get(username='writer')
        self.requester= User.objects.get(username='requester')
    def test_full_name(self):
        self.assertEqual(self.fred.full_name, 'Fred Flintstone')
    def test_writers_property(self):
        self.assertEqual(self.requester.writers, [self.writer, self.fred])
    def test_requesters_property(self):
        self.assertEqual(self.writer.requesters, [self.requester])