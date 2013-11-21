from articles.models import (Article)
from articles.views import (CreateArticle, UpdateArticle)
from articles.forms import (CreateArticleForm, KeywordInlineFormSet, UpdateArticleForm, 
  WriteArticleForm)
from common import BaseTestCase, InstanceOf, BaseTestCaseAsGuest

class TestCreateEditArticle(BaseTestCase):
  fixtures = ['fixtures/test_articles_fixture.json']
  def test_create_simple_article(self):
    response = self.c.get('/articles/article/add/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_edit.html'])
    self.assertContext(response, {
      'form':InstanceOf(CreateArticleForm),
      'inlines':InstanceOf(list),
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
      ),
      'article':None,
      'heading':'New Article',
      'view': InstanceOf(CreateArticle),
    })
    response = self.c.post('/articles/article/add/',{
      'article_type':1,
      'keyword_set-INITIAL_FORMS':0,
      'keyword_set-MAX_NUM_FORMS':1000,
      'keyword_set-TOTAL_FORMS':1,
      'priority':1,
      })
    self.assertEqual(response.status_code, 302)
  def test_owner_edit_unassigned_article(self):
    response = self.c.get('/articles/article/1/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_edit.html'])
    self.assertContext(response, {
      'form':InstanceOf(UpdateArticleForm),
      'inlines':InstanceOf(list),
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
      ),
      'article':Article.objects.get(pk=1),
      'heading':'Unavailable (100 words)',
      'view': InstanceOf(UpdateArticle),
      'object':Article.objects.get(pk=1),
    })
    response = self.c.post('/articles/article/1/',{
      "article_type": 1,
      "extra":"Save",
      "keyword_set-0-id": 1,
      "keyword_set-0-keyword":"Unavailable",
      "keyword_set-0-times":1,
      "keyword_set-0-url":"www.google.com",
      "keyword_set-INITIAL_FORMS":1,
      "keyword_set-MAX_NUM_FORMS":1000,
      "keyword_set-TOTAL_FORMS":3,
      "language": "en",
      "minimum":100,
      "owner":1,
      "priority": 5,
      })
    self.assertEqual(response.status_code, 302)
  def test_owner_edit_assigned_article(self):
    response = self.c.get('/articles/article/6/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_write.html'])
    self.assertContext(response, {
      'form':InstanceOf(WriteArticleForm),
      'inlines':[],
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
      ),
      'article':Article.objects.get(pk=6),
      'heading':'Assigned (100 words)',
      'view': InstanceOf(UpdateArticle),
      'object':Article.objects.get(pk=6),
    })
    # Try saving without typing anything
    response = self.c.post('/articles/article/6/',{
      "body" : "",
      "extra": "done",
      "title": "Assigned",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=6)
    self.assertEqual(a.body, "")
    self.assertEqual(a.title, "Assigned")
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')

    response = self.c.post('/articles/article/6/',{
      "body" : "This is a nice sentance just to test the article.",
      "extra": "done",
      "title": "Assigned Very Well",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=6)
    self.assertEqual(a.body, "This is a nice sentance just to test the article.")
    self.assertEqual(a.title, "Assigned Very Well")
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')
  def test_writer_writes_and_submits_assigned_article(self):
    self.login(username='MyWriter', password="pass")
    response = self.c.get('/articles/article/6/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_write.html'])
    self.assertContext(response, {
      'form':InstanceOf(WriteArticleForm),
      'inlines':[],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'article':Article.objects.get(pk=6),
      'heading':'Assigned (100 words)',
      'view': InstanceOf(UpdateArticle),
      'object':Article.objects.get(pk=6),
    })
    # Write
    response = self.c.post('/articles/article/6/',{
      "body" : "This is a beautiful article.",
      "extra": "done",
      "title": "Amazing",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=6)
    self.assertEqual(a.body, "This is a beautiful article.")
    self.assertEqual(a.title, "Amazing")
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')
    # Write
    response = self.c.post('/articles/article/6/',{
      "body" : "This is a beautiful article. Wait for it...",
      "extra": "autosave",
      "title": "Lets autosave",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=6)
    self.assertEqual(a.body, "This is a beautiful article. Wait for it...")
    self.assertEqual(a.title, "Lets autosave")
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')

    # Edit and Submit
    response = self.c.post('/articles/article/6/',{
      "body" : "This is a beautiful article. Oops I fixed a mistake.",
      "extra": "submit",
      "title": "Amazinger",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=6)
    self.assertEqual(a.body, "This is a beautiful article. Oops I fixed a mistake.")
    self.assertEqual(a.title, "Amazinger")
    self.assertTrue(a.submitted)
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')

  def test_reviewer_reviews_and_approves_submitted_article(self):
    self.login(username='MyReviewer', password="pass")
    response = self.c.get('/articles/article/41/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_write.html'])
    self.assertContext(response, {
      'form':InstanceOf(WriteArticleForm),
      'inlines':[],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'article':Article.objects.get(pk=41),
      'heading':'Assigned to Reviewer',
      'view': InstanceOf(UpdateArticle),
      'object':Article.objects.get(pk=41),
    })
    # Edit
    response = self.c.post('/articles/article/41/',{
      "body" : "This is a good article.",
      "extra": "done",
      "title": "Perfect",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=41)
    self.assertEqual(a.body, "This is a good article.")
    self.assertEqual(a.title, "Perfect")
    self.assertFalse(a.approved)
    self.assertFalse(a.rejected)
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')
    # Edit and Approve
    response = self.c.post('/articles/article/41/',{
      "body" : "This is a better article.",
      "extra": "approve",
      "title": "Perfect article",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=41)
    self.assertEqual(a.body, "This is a better article.")
    self.assertEqual(a.title, "Perfect article")
    self.assertTrue(a.approved)
    self.assertFalse(a.rejected)
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')
    # Edit and Reject
    self.assertFalse(Article.objects.get(pk=42).rejected)
    response = self.c.post('/articles/article/42/',{
      "body" : "This is a horrible article.",
      "extra": "reject",
      "title": "Bad article",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=42)
    self.assertEqual(a.body, "This is a horrible article.")
    self.assertEqual(a.title, "Bad article")
    self.assertTrue(a.rejected)
    self.assertFalse(a.approved)
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')

  def test_owner_views_and_rejects_accepted_article(self):
    response = self.c.get('/articles/article/14/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_write.html'])
    self.assertContext(response, {
      'form':InstanceOf(WriteArticleForm),
      'inlines':InstanceOf(list),
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
      ),
      'article':Article.objects.get(pk=14),
      'heading':'Accepted',
      'view': InstanceOf(UpdateArticle),
      'object':Article.objects.get(pk=14),
    })
    # Edit and Reject
    self.assertFalse(Article.objects.get(pk=14).rejected)
    self.assertTrue(Article.objects.get(pk=14).approved)
    response = self.c.post('/articles/article/14/',{
      "body" : "This is a bad article.",
      "extra": "reject",
      "title": "Horrible article",
      })
    self.assertEqual(response.status_code, 200)
    a=Article.objects.get(pk=14)
    self.assertEqual(a.body, "This is a bad article.")
    self.assertEqual(a.title, "Horrible article")
    self.assertTrue(a.rejected)
    self.assertFalse(a.approved)
    self.assertEqual(unicode(response),u'Vary: Cookie\nContent-Type: text/html; charset=utf-8\n\nAOK.')
    
  def test_create_article_with_another_users_id(self):
    # Should use real users id instead
    self.assertFalse(Article.objects.filter(owner_id=3))
    response = self.c.post('/articles/article/add/',{
      'article_type':1,
      'keyword_set-INITIAL_FORMS':0,
      'keyword_set-MAX_NUM_FORMS':1000,
      'keyword_set-TOTAL_FORMS':1,
      'priority':1,
      'owner':3,
      })
    self.assertEqual(response.status_code, 302)
    self.assertFalse(Article.objects.filter(owner_id=3))

# Test making a new category and project from create article page
# Test only correct buttons appear at the bottom of the write page
# Test wrong writer trying to write, submit
# test wrong reviewer trying to approve
# test wrong reviewer trying to reject
# test wrong user trying to publish
# Test reviewer trying to approve non submitted article
# Test guest trying to edit article