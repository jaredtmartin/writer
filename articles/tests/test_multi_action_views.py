from articles.models import (Article, Writer, Reviewer, ArticleAction, ReviewerGroup, WriterGroup, 
  ACT_SUBMIT, ACT_APPROVE, STATUS_PUBLISHED)
from common import BaseTestCase, InstanceOf, BaseTestCaseAsGuest
from django.core.urlresolvers import reverse

class TestMultiActionViews(BaseTestCase):
  fixtures = ['fixtures/test_articles_fixture.json']
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

class TestMultiActionViewsAsGuest(BaseTestCaseAsGuest):
  fixtures = ['fixtures/test_articles_fixture.json']
  def test_make_article_available_to_writer(self):
    response = self.c.post(reverse('make_available_to_writer'), {'action-select':2, 'writer':3})
  def test_make_article_available_to_reviewer(self):
    response = self.c.post(reverse('make_available_to_reviewer'), {'action-select':2, 'reviewer':6})
  def test_make_article_available_to_all_writers(self):
    response = self.c.post(reverse('make_available_to_all_writers'), {'action-select':2})
  def test_make_article_available_to_all_reviewers(self):
    response = self.c.post(reverse('make_available_to_all_reviewers'), {'action-select':2})
  def test_make_article_available_to_all_my_writers(self):
    response = self.c.post(reverse('make_available_to_all_my_writers'), {'action-select':2})
  def test_make_article_available_to_all_my_reviewers(self):
    response = self.c.post(reverse('make_available_to_all_my_reviewers'), {'action-select':2})
  def test_make_available_to_writer_group(self):
    response = self.c.post(reverse('make_available_to_writer_group'), {'action-select':2,'group':1})
  def test_make_available_to_reviewer_group(self):
    response = self.c.post(reverse('make_available_to_reviewer_group'), {'action-select':2,'group':2})
  def test_make_article_unavailable_to_writers(self):
    response = self.c.post(reverse('make_unavailable_to_writers'), {'action-select':2})
  def test_make_article_unavailable_to_reviewers(self):
    response = self.c.post(reverse('make_unavailable_to_reviewers'), {'action-select':2})
  def test_assign_article_to_writer(self):
    response = self.c.post(reverse('assign_to_writer'), {'action-select':2, 'writer':3})
  def test_assign_article_to_reviewer(self):
    response = self.c.post(reverse('assign_to_reviewer'), {'action-select':2, 'reviewer':6})
  def test_releasing_article_writer_as_writer(self):
    w=Writer.objects.get(writer=self.me)
    Article.objects.filter(pk=27).update(writer=w)
    response = self.c.post(reverse('release_as_writer'), {'action-select':27})
  def test_releasing_article_writer_as_owner(self):
    Article.objects.filter(pk=2).update(writer=Writer.objects.get(pk=3))
    response = self.c.post(reverse('release_as_writer'), {'action-select':2})
  def test_releasing_article_as_reviewer(self):
    Article.objects.filter(pk=2).update(reviewer=Reviewer.objects.get(pk=6))
    response = self.c.post(reverse('release_as_reviewer'), {'action-select':2})
  def test_claiming_article_as_writer(self):
    response = self.c.post(reverse('claim_as_writer'), {'action-select':27})
  def test_claiming_article_as_reviewer(self):
    response = self.c.post(reverse('claim_as_reviewer'), {'action-select':27})
  def test_submitting_article(self):
    Article.objects.filter(pk=27).update(writer=self.me)
    response = self.c.post(reverse('submit_articles'), {'action-select':27})
  def test_rejecting_and_returning_article_to_writer(self):
    w=Writer.objects.get(pk=3)
    u=w.writer
    act = ArticleAction.objects.create(user=u, author=u, code=ACT_SUBMIT)
    Article.objects.filter(pk=2).update(writer=w, submitted=act, body="This is content.",title="This is the title.")
    reason = "You're ugly."
    response = self.c.post(reverse('reject_articles'), {'action-select':2,'reason':reason,'return_to_writer':True})
  def test_rejecting_article_and_making_unavailable(self):
    w=Writer.objects.get(pk=3)
    u=w.writer
    act = ArticleAction.objects.create(user=u, author=u, code=ACT_SUBMIT)
    Article.objects.filter(pk=2).update(writer=w, submitted=act, body="This is content.",title="This is the title.")
    reason = "You're ugly."
    response = self.c.post(reverse('reject_articles'), {'action-select':2,'reason':reason,'return_to_writer':False})
  def test_approving_article(self):
    w=Writer.objects.get(pk=3)
    u=w.writer
    act = ArticleAction.objects.create(user=u, author=u, code=ACT_SUBMIT)
    a = Article.objects.filter(pk=2).update(writer=w, submitted=act)
    response = self.c.post(reverse('approve_articles'), {'action-select':2})
  def test_marking_article_as_published(self):
    w=Writer.objects.get(pk=3)
    u=w.writer
    sub = ArticleAction.objects.create(user=u, author=u, code=ACT_SUBMIT)
    act = ArticleAction.objects.create(user=self.me, author=u, code=ACT_APPROVE)
    a = Article.objects.filter(pk=2).update(writer=w, submitted=sub, approved=act)
    response = self.c.post(reverse('mark_as_published'), {'action-select':2})