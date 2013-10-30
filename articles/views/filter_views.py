from django.views.generic import ListView
from articles.models import (Article, Writer, Reviewer, User, WriterGroup, ReviewerGroup, 
  REQUESTER_MODE, WRITER_MODE, REVIEWER_MODE, STATUS_ASSIGNED, STATUS_SUBMITTED, STATUS_APPROVED,
  STATUS_PUBLISHED)
from django.db.models import Q

class FiltersMixin(object):
  extra_context = {
    "sidebar_links":'get_sidebar_links',
  }
  def filter_approved(self, qs, value=True):
    return qs.filter(status=STATUS_APPROVED)
  def filter_assigned(self, qs, value=True):
    if self.request.user.mode==WRITER_MODE:
      return qs.filter(writer__writer=self.request.user, was_claimed=False, status=STATUS_ASSIGNED)
    elif self.request.user.mode==REQUESTER_MODE:
      return qs.filter(writer__isnull=False, was_claimed=False, status=STATUS_ASSIGNED)
  def filter_available(self, qs, value=True):
    if self.request.user.mode == REQUESTER_MODE:
      return qs.filter(owner=self.request.user).filter(Q(writers__isnull=False)|Q(writer_groups__isnull=False)|Q(available_to_all_writers=True)|Q(available_to_all_my_writers=True)).exclude(writer__isnull=False).distinct()
    elif self.request.user.mode == WRITER_MODE: return qs.filter(Q(writers__writer=self.request.user)|Q(writer_groups__contacts__writer__writer=self.request.user)|Q(available_to_all_writers=True)|Q(available_to_all_my_writers=True, owner__writers__writer=self.request.user)).exclude(writer__isnull=False).distinct()
    elif self.request.user.mode == REVIEWER_MODE: return qs.filter(Q(reviewers__reviewer=self.request.user)|Q(reviewer_groups__contacts__reviewer__reviewer=self.request.user)|Q(available_to_all_reviewers=True)|Q(available_to_all_my_reviewers=True, owner__reviewers__reviewers=self.request.user)).exclude(reviewer__isnull=False).distinct()
  def filter_claimed(self, qs, value=True):
    if self.request.user.mode==WRITER_MODE:
      return qs.filter(writer__writer=self.request.user, was_claimed=True, status=STATUS_ASSIGNED)
    elif self.request.user.mode==REQUESTER_MODE:
      return qs.filter(was_claimed=True, status=STATUS_ASSIGNED)
  def filter_rejected(self, qs, value=True):
    return qs.filter(rejected__isnull=False)
  def filter_published(self, qs, value=True):
    if self.request.user.mode==REQUESTER_MODE: return qs.filter(status=STATUS_PUBLISHED)
    else: return qs.none()
  def filter_submitted(self, qs, value=True):
    if self.request.user.mode==WRITER_MODE:
      return qs.filter(writer__writer=self.request.user, status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
    elif self.request.user.mode==REQUESTER_MODE:
      return qs.filter(status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
  def filter_unavailable(self, qs, value=True):
    return qs.filter(owner=self.request.user, available_to_all_my_writers=False, available_to_all_writers=False, writers__isnull=True, writer_groups__isnull=True, writer=None)
  def filter_my_writers(self, qs, value=True):
    return qs.filter(requester=self.request.user, confirmation = True)
  def filter_writers_pending(self, qs, value=True):
    return qs.filter(requester=self.request.user, confirmation__isnull=True)
  def filter_writers_available(self, qs, value=True):
    return qs.exclude(contacts_as_writer__requester=self.request.user).exclude(pk=self.request.user.pk)
  def filter_my_reviewers(self, qs, value=True):
    return qs.filter(requester=self.request.user, confirmation = True)
  def filter_reviewers_pending(self, qs, value=True):
    return qs.filter(requester=self.request.user, confirmation__isnull=True)
  def filter_reviewers_available(self, qs, value=True):
    return qs.exclude(contacts_as_reviewer__requester=self.request.user).exclude(pk=self.request.user.pk)
  def filter_writer_groups(self, qs, value=True):
    return qs.filter(owner=self.request.user)
  def filter_reviewer_groups(self, qs, value=True):
    return qs.filter(owner=self.request.user)
  def filter_available_to_writer(self, qs, value=[]):
    # print "self.request.GET = %s" % str(self.request.GET)
    # print "value = %s" % str(value)
    if not value: return qs
    for contact in value:
      return qs.filter()
  def get_sidebar_links(self):
    links= (
      ('Articles', (
        ('Unavailable', self.filter_unavailable(Article.objects.all()).count(),False),
        ('Available', self.filter_available(Article.objects.all()).count(),not self.request.user.mode==REQUESTER_MODE),
        ('Assigned', self.filter_assigned(Article.objects.all()).count(),False),
        ('Claimed', self.filter_claimed(Article.objects.all()).count(),False),
        ('Submitted', self.filter_submitted(Article.objects.all()).count(),False),
        ('Approved', self.filter_approved(Article.objects.all()).count(),False),
        ('Rejected', self.filter_rejected(Article.objects.all()).count(),False),
        ('Published', self.filter_published(Article.objects.all()).count(),False),
      )),)
    if self.request.user.mode == REQUESTER_MODE:
      links +=(
        ('Writers', (
          ('My Writers', self.filter_my_writers(Writer.objects.all()).count(),False),
          ('Writers Pending', self.filter_writers_pending(Writer.objects.all()).count(),False),
          ('Writers Avail.', self.filter_writers_available(User.writer_users.all()).count(),True),
          ('Writer Groups', self.filter_writer_groups(WriterGroup.objects.all()).count(),True),
        )),
        ('Reviewers', (
          ('My Reviewers', self.filter_my_reviewers(Reviewer.objects.all()).count(),False),
          ('Reviewers Pending', self.filter_reviewers_pending(Reviewer.objects.all()).count(),False),
          ('Reviewers Avail.', self.filter_reviewers_available(User.reviewer_users.all()).count(),True),
          ('Reviewer Groups', self.filter_reviewer_groups(ReviewerGroup.objects.all()).count(),True),
        )),
      )
    # print "links = %s" % str(links)
    return links
class UpdateFilters(FiltersMixin, ListView):
    template_name = "articles/ajax_article_list_row.html"
    model = Article