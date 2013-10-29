from articles.models import (Article, User, ArticleType, Keyword, WRITER_MODE, REVIEWER_MODE, 
  REQUESTER_MODE, Writer, Reviewer, STATUS_PUBLISHED, ACT_APPROVE)
from newtests.common import *
from articles.views import *
from articles.forms import *
from django.core.urlresolvers import reverse

from newtests.test_filter_views import *

# class BaseTestCase(VanillaBaseTestCase):
#   def login(self):
#     response = self.c.post('/accounts/login/', {'username': 'jared', 'password': 't1bur0n'})
#     # print "User.objects.all().count() = %s" % str(User.objects.all().count())
#     self.assertEqual(response.status_code, 302)
#   def setUp(self):
#     settings.DEBUG = True
#     self.c = Client()
#     self.login()
#     self.me = User.objects.get(pk=1)
#   def assertMessages(self, response, expected):
#     messages = [str(msg) for msg in response.context['messages']]
#     for msg in messages: self.assertTrue(msg in expected, "context contains unexpected message: '%s'" % msg)
#     for msg in expected: self.assertTrue(msg in messages, "context missing message: '%s'" % msg)

class TestArticles(BaseTestCase):
  fixtures = ['fixtures/test_articles_fixture.json']
  def test_avilable_articles_list(self):
    """ Just a simple run through"""
    response = self.c.get('/articles/available/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'reviewer_filter_counts':{'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (1, True), 'My Reviewers': (1, False)},
      'heading':'Available Articles',
      'is_paginated': False,
      'article_filter_counts':{'Available': (7, False), 'Assigned': (3, False), 'Unavailable': (1, False), 'Published': (1, False), 'Claimed': (1, False), 'Approved': (2, False), 'Submitted': (2, False), 'Rejected': (1, False)},
      'hidden_columns':['Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':7,
      'paginator': None,
      'writer_filter_counts':{'My Writers': (1, False), 'Writers Pending': (1, False), 'Writers Avail.': (2, True), 'Writer Groups': (1, True)},
      'article_list':Article.objects.filter(pk__in=[2,3,4,5,8,9,15]),
      'object_list':Article.objects.filter(pk__in=[2,3,4,5,8,9,15]),
      'view': InstanceOf(AvailableArticles),
    })
  def test_make_article_available_to_writer(self):
    response = self.c.post(reverse('make_available_to_writer'), {'action-select':2, 'writer':3})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made available sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Writer.objects.get(pk=3) in Article.objects.get(pk=2).writers.all())
  
  def test_make_article_available_to_reviewer(self):
    response = self.c.post(reverse('make_available_to_reviewer'), {'action-select':2, 'reviewer':6})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made available sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Reviewer.objects.get(pk=6) in Article.objects.get(pk=2).reviewers.all())

  def test_make_article_available_to_all_writers(self):
    response = self.c.post(reverse('make_available_to_all_writers'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made available sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=2).available_to_all_writers)
  
  def test_make_article_available_to_all_reviewers(self):
    response = self.c.post(reverse('make_available_to_all_reviewers'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made available sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=2).available_to_all_reviewers)

  def test_make_article_available_to_all_my_writers(self):
    response = self.c.post(reverse('make_available_to_all_my_writers'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made available sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=2).available_to_all_my_writers)

  def test_make_article_available_to_all_my_reviewers(self):
    response = self.c.post(reverse('make_available_to_all_my_reviewers'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made available sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=2).available_to_all_my_reviewers)

  def test_make_available_to_writer_group(self):
    response = self.c.post(reverse('make_available_to_writer_group'), {'action-select':2,'group':1})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made available sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(WriterGroup.objects.get(pk=1) in Article.objects.get(pk=2).writer_groups.all())

  def test_make_available_to_reviewer_group(self):
    response = self.c.post(reverse('make_available_to_reviewer_group'), {'action-select':2,'group':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made available sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(ReviewerGroup.objects.get(pk=2) in Article.objects.get(pk=2).reviewer_groups.all())

  def test_make_article_unavailable_to_writers(self):
    response = self.c.post(reverse('make_unavailable_to_writers'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made unavailable sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    a=Article.objects.get(pk=2)
    self.assertTrue(not a.available_to_all_writers)
    self.assertEqual(a.writers.count(),0)
    self.assertEqual(a.writer_groups.count(),0)
    self.assertTrue(not a.available_to_all_my_writers)
  def test_make_article_unavailable_to_reviewers(self):
    response = self.c.post(reverse('make_unavailable_to_reviewers'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been made unavailable sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(not Article.objects.get(pk=2).available_to_all_reviewers)
    self.assertEqual(Article.objects.get(pk=2).reviewers.count(),0)
    self.assertEqual(Article.objects.get(pk=2).reviewer_groups.count(),0)
    self.assertTrue(not Article.objects.get(pk=2).available_to_all_my_reviewers)

  def test_assign_article_to_writer(self):
    response = self.c.post(reverse('assign_to_writer'), {'action-select':2, 'writer':3})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been assigned sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=2).writer==Writer.objects.get(pk=3))

  def test_assign_article_to_reviewer(self):
    response = self.c.post(reverse('assign_to_reviewer'), {'action-select':2, 'reviewer':6})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been assigned sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=2).reviewer==Reviewer.objects.get(pk=6))

  def test_releasing_article_writer_as_writer(self):
    w=Writer.objects.get(writer=self.me)
    Article.objects.filter(pk=27).update(writer=w)
    response = self.c.post(reverse('release_as_writer'), {'action-select':27})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been released sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=27),
      'as_row':True,
      })
    self.assertFalse(Article.objects.get(pk=27).writer)

  def test_releasing_article_writer_as_owner(self):
    Article.objects.filter(pk=2).update(writer=Writer.objects.get(pk=3))
    response = self.c.post(reverse('release_as_writer'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been released sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertFalse(Article.objects.get(pk=2).writer)

  def test_releasing_article_as_reviewer(self):
    Article.objects.filter(pk=2).update(reviewer=Reviewer.objects.get(pk=6))
    response = self.c.post(reverse('release_as_reviewer'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been released sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertFalse(Article.objects.get(pk=2).reviewer)

  def test_claiming_article_as_writer(self):
    response = self.c.post(reverse('claim_as_writer'), {'action-select':27})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been claimed sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=27),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=27).writer==Writer.objects.get(pk=7))

  def test_claiming_article_as_reviewer(self):
    response = self.c.post(reverse('claim_as_reviewer'), {'action-select':27})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been claimed sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=27),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=27).reviewer==Reviewer.objects.get(pk=9))

  def test_submitting_article(self):
    Article.objects.filter(pk=27).update(writer=self.me)
    response = self.c.post(reverse('submit_articles'), {'action-select':27})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been submitted sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=27),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=27).submitted)

  def test_rejecting_and_returning_article_to_writer(self):
    w=Writer.objects.get(pk=3)
    u=w.writer
    act = ArticleAction.objects.create(user=u, author=u, code=ACT_SUBMIT)
    Article.objects.filter(pk=2).update(writer=w, submitted=act, body="This is content.",title="This is the title.")
    reason = "You're ugly."
    response = self.c.post(reverse('reject_articles'), {'action-select':2,'reason':reason,'return_to_writer':True})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been rejected sucessfully.'])
    a=Article.objects.filter(pk=2)
    self.assertContext(response, {
      'object_list': a,
      'as_row':True,
      })
    a=a[0]
    self.assertTrue(a.rejected)
    self.assertTrue(a.rejected.comment==reason)
    self.assertTrue(a.writer==w)
    self.assertTrue(a.body=="This is content.")
    self.assertTrue(a.title=="This is the title.")

  def test_rejecting_article_and_making_unavailable(self):
    w=Writer.objects.get(pk=3)
    u=w.writer
    act = ArticleAction.objects.create(user=u, author=u, code=ACT_SUBMIT)
    Article.objects.filter(pk=2).update(writer=w, submitted=act, body="This is content.",title="This is the title.")
    reason = "You're ugly."
    response = self.c.post(reverse('reject_articles'), {'action-select':2,'reason':reason,'return_to_writer':False})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been rejected sucessfully.'])
    a=Article.objects.filter(pk=2)
    self.assertContext(response, {
      'object_list': a,
      'as_row':True,
      })
    a=a[0]
    self.assertTrue(a.rejected)
    self.assertTrue(a.rejected.comment==reason)
    self.assertFalse(a.writer)
    self.assertTrue(a.body=="")
    self.assertTrue(a.title=="")

  def test_approving_article(self):
    w=Writer.objects.get(pk=3)
    u=w.writer
    act = ArticleAction.objects.create(user=u, author=u, code=ACT_SUBMIT)
    a = Article.objects.filter(pk=2).update(writer=w, submitted=act)
    response = self.c.post(reverse('approve_articles'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been approved sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=2).approved)

  def test_marking_article_as_published(self):
    w=Writer.objects.get(pk=3)
    u=w.writer
    sub = ArticleAction.objects.create(user=u, author=u, code=ACT_SUBMIT)
    act = ArticleAction.objects.create(user=self.me, author=u, code=ACT_APPROVE)
    a = Article.objects.filter(pk=2).update(writer=w, submitted=sub, approved=act)
    response = self.c.post(reverse('mark_as_published'), {'action-select':2})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["articles/ajax_article_list_row.html"])
    self.assertMessages(response,['The article has been marked as published sucessfully.'])
    self.assertContext(response, {
      'object_list': Article.objects.filter(pk=2),
      'as_row':True,
      })
    self.assertTrue(Article.objects.get(pk=2).status==STATUS_PUBLISHED)
# Test sombody else's rejected doesnt appear in my view since I'm rewriting it

# Test article.writer_status
# Test article.reviewer_status


################################################################################
       ###   ###  #   # #####   #    ###  #####  ####
      #   # #   # ##  #   #    # #  #   #   #   #    
      #     #   # # # #   #    ###  #       #    ### 
      #   # #   # #  ##   #   #   # #   #   #       #
       ###   ###  #   #   #   #   #  ###    #   #### 
################################################################################

class TestContacts(BaseTestCase):
  fixtures = ['fixtures/test_contacts_fixture.json']
  def test_list_available_writers(self):
    response = self.c.get(reverse('writers avail.'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/user_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'heading': 'Available Writers', 
      'is_paginated': False, 
      'object_list': User.objects.filter(pk__in=[2,3]), 
      'page_obj': None, 
      'paginator': None, 
      'position': 1, 
      'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/user_row.html', 
      'user_list': User.objects.filter(pk__in=[2,3]), 
      'view': InstanceOf(ListAvailableWriters), 
      'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_pending_writers(self):
    response = self.c.get(reverse('writers pending'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/contact_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'heading': 'Writers Pending Approval', 
      'is_paginated': False, 
      'object_list': Writer.objects.filter(pk=2), 
      'page_obj': None, 
      'paginator': None,
      'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/worker_row.html', 
      'writer_list': Writer.objects.filter(pk=2), 
      'view': InstanceOf(ListPendingWriters), 
      'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_my_writers(self):
    response = self.c.get(reverse('my writers'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/contact_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'heading': 'My Writers', 
      'is_paginated': False, 
      'object_list': Writer.objects.filter(pk=3), 
      'page_obj': None, 
      'paginator': None,
      'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/worker_row.html', 
      'writer_list': Writer.objects.filter(pk=3), 
      'view': InstanceOf(ListMyWriters), 
      'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_available_reviewers(self):
    response = self.c.get(reverse('reviewers avail.'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/user_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'heading': 'Available Reviewers', 
      'is_paginated': False, 
      'object_list': User.objects.filter(pk__in=[6,7]), 
      'page_obj': None, 
      'paginator': None, 
      'position': 2, 
      'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/user_row.html', 
      'user_list': User.objects.filter(pk__in=[6,7]), 
      'view': InstanceOf(ListAvailableReviewers), 
      'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_pending_reviewers(self):
    response = self.c.get(reverse('reviewers pending'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/contact_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'heading': 'Reviewers Pending Approval', 
      'is_paginated': False, 
      'object_list': Reviewer.objects.filter(pk=5), 
      'page_obj': None, 
      'paginator': None,
      'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/worker_row.html', 
      'reviewer_list': Reviewer.objects.filter(pk=5), 
      'view': InstanceOf(ListPendingReviewers), 
      'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_my_reviewers(self):
    response = self.c.get(reverse('my reviewers'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/contact_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'heading': 'My Reviewers', 
      'is_paginated': False, 
      'object_list': Reviewer.objects.filter(pk=6), 
      'page_obj': None, 
      'paginator': None,
      'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/worker_row.html', 
      'reviewer_list': Reviewer.objects.filter(pk=6), 
      'view': InstanceOf(ListMyReviewers), 
      'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_create_writer(self):
    u=User.objects.create(username="New Writer")
    response = self.c.post(reverse('create_writer'),{'requester':1, 'writer':u.pk})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["design/ajax_row.html"])
    self.assertMessages(response,['Your request is awaiting approval from the other user.'])
    self.assertContext(response, {
      'object': u,
      'form':InstanceOf(WriterForm),
      'hide_row':True, 
      'writer':u,
      'row_template_name':'articles/user_row.html',
      'view':InstanceOf(CreateWriter),
      })
  def test_create_reviewer(self):
    u=User.objects.create(username="New Reviewer")
    response = self.c.post(reverse('create_reviewer'),{'requester':'1', 'reviewer':u.pk})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["design/ajax_row.html"])
    self.assertMessages(response,['Your request is awaiting approval from the other user.'])
    self.assertContext(response, {
      'form':InstanceOf(ReviewerForm),
      'object':u,
      'hide_row':True, 
      'reviewer':u,
      'row_template_name':'articles/user_row.html',
      'view':InstanceOf(CreateReviewer),
    })
  def test_confirm_writer(self):
    u=User.objects.create(username="New Writer")
    c=Writer.objects.create(requester=self.me, writer=u, user_asked=self.me)
    response = self.c.post(reverse('confirm_contact', kwargs={'pk':c.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["design/ajax_row.html"])
    self.assertMessages(response,['The contact has been confirmed successfully.'])
    self.assertContext(response, {
      'object': Contact.objects.get(pk=c.pk),
      'hide_row':True, 
      'contact':Contact.objects.get(pk=c.pk),
      'row_template_name':'articles/worker_row.html',
      'view':InstanceOf(ConfirmContact),
      })
  def test_confirm_reviewer(self):
    u=User.objects.create(username="New Reviewer")
    c=Reviewer.objects.create(requester=self.me, reviewer=u, user_asked=self.me)
    response = self.c.post(reverse('confirm_contact', kwargs={'pk':c.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["design/ajax_row.html"])
    self.assertMessages(response,['The contact has been confirmed successfully.'])
    self.assertContext(response, {
      'object':Contact.objects.get(pk=c.pk),
      'hide_row':True, 
      'contact':Contact.objects.get(pk=c.pk),
      'row_template_name':'articles/worker_row.html',
      'view':InstanceOf(ConfirmContact),
    })
  def test_delete_writer(self):
    u=User.objects.create(username="New Writer")
    c=Writer.objects.create(requester=self.me, writer=u, user_asked=self.me)
    pk=c.pk
    response = self.c.post(reverse('delete_contact', kwargs={'pk':c.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["design/ajax_row.html"])
    self.assertMessages(response,['The contact has been deleted.'])
    self.assertContext(response, {
      'object': Contact(pk=pk),
      'hide_row':True, 
      'contact':Contact(pk=pk),
      'row_template_name':'articles/worker_row.html',
      'view':InstanceOf(DeleteContact),
      })
  def test_delete_reviewer(self):
    u=User.objects.create(username="New Reviewer")
    c=Reviewer.objects.create(requester=self.me, reviewer=u, user_asked=self.me)
    pk=c.pk
    response = self.c.post(reverse('delete_contact', kwargs={'pk':c.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["design/ajax_row.html"])
    self.assertMessages(response,['The contact has been deleted.'])
    # for msg in response.context['messages']: print msg
    self.assertContext(response, {
      'object':Contact(pk=pk),
      'hide_row':True, 
      'contact':Contact(pk=pk),
      'row_template_name':'articles/worker_row.html',
      'view':InstanceOf(DeleteContact),
    })
  def test_cancel_contact_request(self):
    u=User.objects.create(username="New Reviewer")
    c=Reviewer.objects.create(requester=self.me, reviewer=u, user_asked=self.me)
    pk=c.pk
    response = self.c.post(reverse('cancel_contact_request', kwargs={'pk':c.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["design/ajax_row.html"])
    self.assertMessages(response,["The contact request has been canceled."])
    # for msg in response.context['messages']: print msg
    self.assertContext(response, {
      'object':Contact(pk=pk),
      'hide_row':True, 
      'contact':Contact(pk=pk),
      'row_template_name':'articles/worker_row.html',
      'view':InstanceOf(DeleteContact),
    })
  def test_reject_contact_request(self):
    u=User.objects.create(username="New Reviewer")
    c=Reviewer.objects.create(requester=self.me, reviewer=u, user_asked=self.me)
    pk=c.pk
    response = self.c.post(reverse('reject_contact_request', kwargs={'pk':c.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ["design/ajax_row.html"])
    self.assertMessages(response,["The contact request has been rejected."])
    # for msg in response.context['messages']: print msg
    self.assertContext(response, {
      'object':Contact(pk=pk),
      'hide_row':True, 
      'contact':Contact(pk=pk),
      'row_template_name':'articles/worker_row.html',
      'view':InstanceOf(DeleteContact),
    })

