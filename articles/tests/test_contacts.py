from articles.models import (User, Reviewer, Writer, Contact)
from articles.forms import (ReviewerForm, WriterForm)
from articles.views import (ListAvailableReviewers, ConfirmContact, CreateWriter, CreateReviewer, 
  DeleteContact, ListAvailableReviewers, ListAvailableWriters, ListMyWriters, ListMyReviewers,
  ListPendingWriters, ListPendingReviewers)
from common import BaseTestCase, InstanceOf
from django.core.urlresolvers import reverse

class TestContacts(BaseTestCase):
  fixtures = ['fixtures/test_contacts_fixture.json']
  def test_list_available_writers(self):
    response = self.c.get(reverse('writers avail.'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/user_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      # 'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'sidebar_links': (('Articles', (('Unavailable', 0, False), ('Available', 0, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 0, False), ('Rejected', 0, False), ('Published', 0, False))),),
      'heading': 'Available Writers', 
      'is_paginated': False, 
      'object_list': User.objects.filter(pk__in=[2,3]), 
      'page_obj': None, 
      'paginator': None, 
      'position': 1, 
      # 'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/user_row.html', 
      'user_list': User.objects.filter(pk__in=[2,3]), 
      'view': InstanceOf(ListAvailableWriters), 
      # 'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_pending_writers(self):
    response = self.c.get(reverse('writers pending'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/contact_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      # 'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'sidebar_links': (('Articles', (('Unavailable', 0, False), ('Available', 0, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 0, False), ('Rejected', 0, False), ('Published', 0, False))),),
      'heading': 'Writers Pending Approval', 
      'is_paginated': False, 
      'object_list': Writer.objects.filter(pk=2), 
      'page_obj': None, 
      'paginator': None,
      # 'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/worker_row.html', 
      'writer_list': Writer.objects.filter(pk=2), 
      'view': InstanceOf(ListPendingWriters), 
      # 'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_my_writers(self):
    response = self.c.get(reverse('my writers'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/contact_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      # 'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'sidebar_links': (('Articles', (('Unavailable', 0, False), ('Available', 0, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 0, False), ('Rejected', 0, False), ('Published', 0, False))),),
      'heading': 'My Writers', 
      'is_paginated': False, 
      'object_list': Writer.objects.filter(pk=3), 
      'page_obj': None, 
      'paginator': None,
      # 'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/worker_row.html', 
      'writer_list': Writer.objects.filter(pk=3), 
      'view': InstanceOf(ListMyWriters), 
      # 'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_available_reviewers(self):
    response = self.c.get(reverse('reviewers avail.'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/user_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      # 'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'sidebar_links': (('Articles', (('Unavailable', 0, False), ('Available', 0, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 0, False), ('Rejected', 0, False), ('Published', 0, False))),),
      'heading': 'Available Reviewers', 
      'is_paginated': False, 
      'object_list': User.objects.filter(pk__in=[6,7]), 
      'page_obj': None, 
      'paginator': None, 
      'position': 2, 
      # 'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/user_row.html', 
      'user_list': User.objects.filter(pk__in=[6,7]), 
      'view': InstanceOf(ListAvailableReviewers), 
      # 'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_pending_reviewers(self):
    response = self.c.get(reverse('reviewers pending'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/contact_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      # 'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'sidebar_links': (('Articles', (('Unavailable', 0, False), ('Available', 0, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 0, False), ('Rejected', 0, False), ('Published', 0, False))),),
      'heading': 'Reviewers Pending Approval', 
      'is_paginated': False, 
      'object_list': Reviewer.objects.filter(pk=5), 
      'page_obj': None, 
      'paginator': None,
      # 'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/worker_row.html', 
      'reviewer_list': Reviewer.objects.filter(pk=5), 
      'view': InstanceOf(ListPendingReviewers), 
      # 'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
      })
  def test_list_my_reviewers(self):
    response = self.c.get(reverse('my reviewers'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/contact_list.html'])
    self.assertMessages(response,[])
    self.assertContext(response, {
      # 'article_filter_counts': {'Available': (0, True), 'Assigned': (0, False), 'Unavailable': (0, False), 'Published': (0, False), 'Claimed': (0, False), 'Approved': (0, False), 'Submitted': (0, False), 'Rejected': (0, False)}, 
      'sidebar_links': (('Articles', (('Unavailable', 0, False), ('Available', 0, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 0, False), ('Rejected', 0, False), ('Published', 0, False))),),
      'heading': 'My Reviewers', 
      'is_paginated': False, 
      'object_list': Reviewer.objects.filter(pk=6), 
      'page_obj': None, 
      'paginator': None,
      # 'reviewer_filter_counts': {'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (0, True), 'My Reviewers': (1, False)}, 
      'row_template_name': 'articles/worker_row.html', 
      'reviewer_list': Reviewer.objects.filter(pk=6), 
      'view': InstanceOf(ListMyReviewers), 
      # 'writer_filter_counts': {'My Writers': (1, False), 'Writer Groups': (0, True), 'Writers Avail.': (2, True), 'Writers Pending': (1, False)}
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