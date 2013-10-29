import slick.views as slick
from django.views.generic.base import View, TemplateResponseMixin
from articles.models import Article, ArticleAction, ACT_SUBMIT, ACT_REJECT, ACT_APPROVE, User
from articles.forms import (RejectForm, PublishForm, WriterForm, AssignToForm, 
  STATUS_NEW, STATUS_RELEASED, STATUS_ASSIGNED, STATUS_SUBMITTED, STATUS_APPROVED, STATUS_PUBLISHED,
  WriterChoiceForm, ReviewerChoiceForm, WriterGroupChoiceForm, ReviewerGroupChoiceForm)
from django.contrib import messages
from django.db.models import Q

class ArticleActionsView(TemplateResponseMixin, View):
  template_name = "articles/ajax_article_list_row.html"
  model = Article
  next_status = None
  action_property_name=None
  past_tense_action_verb=None
  action_verb=None
  action_form_class = None
  pks=[]
  def filter_by_owner(self, qs):
    if not self.request.user.is_authenticated(): return qs.none()
    if not self.request.user.is_staff: return qs.filter(owner_id=user.pk)
    else: return qs
  def filter_by_writer(self, qs):
    if not self.request.user.is_authenticated(): return qs.none()
    return qs.filter(writer__writer_id=self.request.user.pk)
  def filter_by_owner_or_writer(self, qs):
    if not self.request.user.is_authenticated(): return qs.none()
    if not self.request.user.is_staff: return qs.filter(Q(owner_id=self.request.user.pk)|Q(writer__writer_id=self.request.user.pk))
    else: return qs
  def filter_by_owner_or_reviewer(self, qs):
    if not self.request.user.is_authenticated(): return qs.none()
    if not self.request.user.is_staff: return qs.filter(Q(owner_id=self.request.user.pk)|Q(reviewer__reviewer_id=self.request.user.pk))
    else: return qs
  def filter_by_writer(self, qs):
    if not self.request.user.is_authenticated(): return qs.none()
    if not self.request.user.is_staff: return qs.filter(writer__writer_id=self.request.user.pk)
    else: return qs
  def filter_by_owner_or_writer_or_reviewer(self, qs):
    if not self.request.user.is_authenticated(): return qs.none()
    if not self.request.user.is_staff: return qs.filter(Q(writer__writer_id=self.request.user.pk)|Q(reviewer__reviewer_id=self.request.user.pk))
    else: return qs
  def get_action_property_name(self):
    return self.action_property_name or self.action_verb+'ed'
  def filter_action_queryset(self, qs):
    return qs
  def get_action_form_class(self):
    return self.action_form_class
  def get_requested_objects(self):
    if not self.pks:
      if 'select-across' in self.request.POST and self.request.POST['select-across'] == u'0':
        # Building a empty queryset to load pickled data
        qs = self.model.objects.all()#[:1]
        qs.query = pickle.loads(self.request.session['serialized_qs'])
      else:
        # select a specific set of items
        qs = self.model.objects.filter(pk__in=(self.request.POST.getlist('action-select')))
      self.pks = list(qs.values_list('id', flat=True))
    else: qs=Article.all_objects.filter(pk__in=self.pks)
    return qs

  def get_action_queryset(self):
    try:
      if self.action_qs: return self.action_qs
    except AttributeError: pass
    qs = self.get_requested_objects()
    self.initial_action_qty = len(qs)
    if self.initial_action_qty:
      qs=self.filter_action_queryset(qs)
      self.final_qty = qs.count()
      return qs
    else:
      self.final_qty = 0
      return []

  def create_action(self):pass
  def update_status(self):
    if self.next_status: self.action_qs.update(status=self.next_status)
  def update_articles(self):
    self.update_status()
    if self.action:
      self.action_qs.update(**{'last_action':self.action})
      try:self.action_qs.update(**{self.get_action_property_name():self.action})
      except :pass
  def get_action_verb(self):
    return self.action_verb
  def get_past_tense_action_verb(self):
    if self.past_tense_action_verb: return self.past_tense_action_verb
    return str(self.get_action_verb())+'ed'
  def send_result_messages(self):
    if self.final_qty==0:
      messages.error(self.request, 'The articles selected are not ready to be %s or are not yours to %s.' % (self.get_past_tense_action_verb(), self.get_action_verb()))
    elif self.action_form and not self.action_form.is_valid():
      messages.error(self.request, 'You did not select a valid value to complete this action.')
    elif self.final_qty < self.initial_action_qty:
      messages.warning(self.request, 'Only %i of the articles selected have been %s. Please verify the operation and that you have authority to make this change on the remaining articles.' % (self.final_qty, self.get_past_tense_action_verb()))
    else: 
      if self.final_qty == self.initial_action_qty ==1:
        messages.success(self.request,'The article has been %s sucessfully.' % self.get_past_tense_action_verb())
      elif self.final_qty == self.initial_action_qty ==2:
        messages.success(self.request,'Both of the articles have been %s sucessfully.' % self.get_past_tense_action_verb())
      else:
        messages.success(self.request, 'All (%s) of the articles have been %s sucessfully.' % (self.final_qty, self.get_past_tense_action_verb()))
  def post(self, request, *args, **kwargs):
    self.action_qs = self.get_action_queryset()
    form_class=self.get_action_form_class()
    if self.action_qs and self.final_qty > 0:
      if form_class: self.action_form=form_class(self.request.POST)
      else: self.action_form=None
      if (not self.action_form) or self.action_form.is_valid():
        self.action=self.create_action()
        self.update_articles()
        self.action_qs=self.get_requested_objects()
    elif form_class: self.action_form=form_class()
    self.send_result_messages()
    context = self.get_context_data()
    return self.render_to_response(context)
  def get_context_data(self, **kwargs):
    kwargs.update({'as_row':True,'object_list':self.action_qs})
    return kwargs

############################### Reject Actions ####################################

class RejectArticles(ArticleActionsView):
    action_verb="reject"
    action_form_class = RejectForm
    next_status = STATUS_RELEASED
    action_property_name = "XXX" # This is to disable automatic assigning of property. We'll do this ourself.
    def filter_action_queryset(self, qs):
        qs=qs.filter(submitted__isnull=False)
        return self.filter_by_owner_or_reviewer(qs)
    def create_action(self):
        self.authors = [User.objects.get(pk=w) for w in self.action_qs.values_list('writer', flat=True)]
        for author in self.authors:
            action = ArticleAction.objects.create(
                user=self.request.user, 
                code=ACT_REJECT, 
                comment=self.action_form.cleaned_data['reason'],
                author=author,
            )
            self.action_qs.filter(writer=author).update(rejected=action)
    def update_status(self):
        if self.action_form.cleaned_data['return_to_writer']: self.next_status = STATUS_ASSIGNED
        else: self.next_status = STATUS_RELEASED
        super(RejectArticles, self).update_status()
    def update_articles(self):
        super(RejectArticles, self).update_articles()
        self.action_qs = Article.objects.filter(pk__in=list(self.action_qs.values_list('id', flat=True)))
        self.action_qs.update(submitted=None, approved=None)
        # print "qs[0].writer = %s" % str(qs[0].writer)
        if not self.action_form.cleaned_data['return_to_writer']: 
            self.action_qs.update(writer=None)
            self.action_qs.update(body="")
            self.action_qs.update(title="")

        # print "qs[0].writer = %s" % str(qs[0].writer)
############################### Approve Actions ####################################

class ApproveArticles(ArticleActionsView):
    action_verb="approve"
    action_property_name="approved"
    past_tense_action_verb="approved"
    next_status = STATUS_APPROVED
    def filter_action_queryset(self, qs):
        qs=qs.filter(submitted__isnull=False)
        return self.filter_by_owner_or_reviewer(qs)
    def create_action(self):
        return ArticleAction.objects.create(
            user=self.request.user, 
            code=ACT_APPROVE
        )
############################### Publish Articles ####################################
class MarkArticlesAsPublished(ArticleActionsView):
    next_status = STATUS_PUBLISHED
    action_verb="mark as published"
    past_tense_action_verb="marked as published"
    def filter_action_queryset(self, qs):
        qs=qs.filter(approved__isnull=False)
        return self.filter_by_owner(qs)

class PublishArticles(MarkArticlesAsPublished):
    action_verb="publish"
    action_form_class = PublishForm
    next_status = STATUS_PUBLISHED
    def create_action(self):
        outlet = self.action_form.cleaned_data['outlet']
        outlet.do_action(self.action_qs)
        
############################### Submit Actions ####################################

class SubmitArticles(ArticleActionsView):
  action_verb="submit"
  action_property_name="submitted"
  past_tense_action_verb = "submitted"
  next_status = STATUS_SUBMITTED
  def filter_action_queryset(self, qs):
    qs=qs.filter(submitted__isnull=True)
    # print "qs = %s" % str(qs)
    qs=Article.filter_valid(qs, self.request)
    # print "qs = %s" % str(qs)
    return self.filter_by_writer(qs)
  def create_action(self):
    return ArticleAction.objects.create(
      user=self.request.user, 
      author=self.request.user, 
      code=ACT_SUBMIT, 
    )
  def update_articles(self):
    super(SubmitArticles, self).update_articles()
    self.action_qs.update(rejected=None)
############################### Delete Actions ####################################

class DeleteArticles(ArticleActionsView):
    action_verb="delete"
    action_property_name="deleted"
    def filter_action_queryset(self, qs):
        # Make sure user has permission to submit the articles
        qs=qs.filter(submitted__isnull=True)
        qs = self.filter_by_owner(qs)
        return qs
    def create_action(self):
        return True
    def update_articles(self):
        l=list(qs.values_list('id', flat=True))
        self.action_qs=Article.all_objects.filter(pk__in=l)
        super(DeleteArticles, self).update_articles(qs, action)

############################### Claim Actions ##################################
class Claim(ArticleActionsView):
  action_verb="claim"

class ClaimAsWriter(Claim):
  next_status = STATUS_ASSIGNED
  def update_articles(self):
    super(ClaimAsWriter, self).update_articles()
    for article in self.action_qs:
      writer=article.owner.writers.get(writer=self.request.user)
      article.writer=writer
      article.was_claimed = True
      article.save()
  def filter_action_queryset(self, qs):
    return qs.filter(owner__writers__writer=self.request.user)

class ClaimAsReviewer(Claim):
  def update_articles(self):
    super(ClaimAsReviewer, self).update_articles()
    for article in self.action_qs:
      reviewer=article.owner.reviewers.get(reviewer=self.request.user)
      article.reviewer=reviewer
      article.was_claimed = True
      article.save()
  def filter_action_queryset(self, qs):
    return qs.filter(owner__reviewers__reviewer=self.request.user)

############################### Release Actions ##################################
class Release(ArticleActionsView):
  action_verb="release"
  past_tense_action_verb="released"
  next_status = STATUS_RELEASED
class ReleaseAsWriter(Release):
  def filter_action_queryset(self, qs):
    qs = qs.filter(writer__isnull=False, submitted__isnull=True)
    return self.filter_by_owner_or_writer(qs)
  def update_articles(self):
    super(ReleaseAsWriter, self).update_articles()
    self.action_qs.update(writer=None, was_claimed=False)
class ReleaseAsReviewer(Release):
  def filter_action_queryset(self, qs):
    qs = qs.filter(reviewer__isnull=False, submitted__isnull=True)
    return self.filter_by_owner_or_writer(qs)
  def update_articles(self):
    super(ReleaseAsReviewer, self).update_articles()
    self.action_qs.update(reviewer=None, was_claimed=False)
############################### Available Actions ##################################
# class MakeAvailable(ArticleActionsView):
#     action_verb="make available"
#     past_tense_action_verb="made available"
#     def filter_action_queryset(self, qs):
#         return self.filter_by_owner(qs)

# class MakeAvailableToContact(MakeAvailable):
#   action_form_class = ContactForm
# class MakeAvailableToWriter(MakeAvailable):
#   next_status = STATUS_RELEASED
#   def update_articles(self):
#     super(MakeAvailableToWriter, self).update_articles()
#     self.action_qs.update(available_to_writers=self.action_form.cleaned_data['name'])
#     self.action_qs.update(writer=None, was_claimed=False)
class MakeAvailable(ArticleActionsView):
  action_verb="make available"
  past_tense_action_verb="made available"
  def filter_action_queryset(self, qs):
    return self.filter_by_owner(qs)

class MakeAvailableToWriter(MakeAvailable):
  action_form_class = WriterChoiceForm
  next_status = STATUS_RELEASED
  def update_articles(self):
    super(MakeAvailableToWriter, self).update_articles()
    writer = self.action_form.cleaned_data['writer']
    writer.articles_available_to_me_to_write = writer.articles_available_to_me_to_write.all()|self.action_qs
    self.action_qs.update(writer=None, was_claimed=False, available_to_all_my_writers=False, available_to_all_writers=False)

class MakeAvailableToAllMyWriters(MakeAvailable):
  next_status = STATUS_RELEASED
  def update_articles(self):
    super(MakeAvailableToAllMyWriters, self).update_articles()
    self.action_qs.update(available_to_all_my_writers=True, available_to_all_writers=False, writer=None, was_claimed=False)

class MakeAvailableToAllWriters(MakeAvailable):
  next_status = STATUS_RELEASED
  def update_articles(self):
    super(MakeAvailableToAllWriters, self).update_articles()
    self.action_qs.update(available_to_all_writers=True, writer=None, was_claimed=False)

class MakeAvailableToWriterGroup(MakeAvailable):
  action_form_class = WriterGroupChoiceForm
  next_status = STATUS_RELEASED
  def update_articles(self):
    super(MakeAvailableToWriterGroup, self).update_articles()
    group = self.action_form.cleaned_data['group']
    group.articles_available_to_group_to_write = group.articles_available_to_group_to_write.all()|self.action_qs
    self.action_qs.update(writer=None, was_claimed=False, available_to_all_my_writers=False, available_to_all_writers=False)

class MakeAvailableToReviewer(MakeAvailable):
  action_form_class = ReviewerChoiceForm
  def update_articles(self):
    super(MakeAvailableToReviewer, self).update_articles()
    reviewer = self.action_form.cleaned_data['reviewer']
    reviewer.articles_available_to_me_to_review = reviewer.articles_available_to_me_to_review.all()|self.action_qs
    self.action_qs.update(reviewer=None, available_to_all_my_reviewers=False, available_to_all_reviewers=False)

class MakeAvailableToReviewerGroup(MakeAvailable):
  action_form_class = ReviewerGroupChoiceForm
  def update_articles(self):
    super(MakeAvailableToReviewerGroup, self).update_articles()
    group = self.action_form.cleaned_data['group']
    group.articles_available_to_group_to_review = group.articles_available_to_group_to_review.all()|self.action_qs
    self.action_qs.update(reviewer=None, available_to_all_my_reviewers=False, available_to_all_reviewers=False)

class MakeAvailableToAllMyReviewers(MakeAvailable):
  def update_articles(self):
    super(MakeAvailableToAllMyReviewers, self).update_articles()
    self.action_qs.update(reviewer=None, available_to_all_my_reviewers=True, available_to_all_reviewers=False)

class MakeAvailableToAllReviewers(MakeAvailable):
  def update_articles(self):
    super(MakeAvailableToAllReviewers, self).update_articles()
    self.action_qs.update(available_to_all_reviewers=True, reviewer=None, was_claimed=False)
############################### Unavailable Actions ##################################
class MakeUnavailable(ArticleActionsView):
  action_verb="make unavailable"
  past_tense_action_verb="made unavailable"
  def filter_action_queryset(self, qs):
      return self.filter_by_owner(qs)

class MakeUnavailableToWriters(MakeUnavailable):
  next_status = STATUS_NEW
  def update_articles(self):
    super(MakeUnavailableToWriters, self).update_articles()
    for article in self.action_qs: 
      article.writers.clear()
      article.writer_groups.clear()
    self.action_qs.update(writer=None, was_claimed=False, available_to_all_my_writers=False, available_to_all_writers=False)

class MakeUnavailableToReviewers(MakeUnavailable):
  def update_articles(self):
    super(MakeUnavailableToReviewers, self).update_articles()
    for article in self.action_qs: 
      article.reviewers.clear()
      article.reviewer_groups.clear()
    self.action_qs.update(reviewer=None, was_claimed=False, available_to_all_my_reviewers=False, available_to_all_reviewers=False)
############################### Assign Actions ##################################
class Assign(ArticleActionsView):
    action_verb="assign"
    def filter_action_queryset(self, qs):
        return self.filter_by_owner(qs)
class AssignToWriter(Assign):
    action_form_class = WriterChoiceForm
    next_status = STATUS_ASSIGNED
    def update_articles(self):
        super(AssignToWriter, self).update_articles()
        self.action_qs.update(writer=self.action_form.cleaned_data['writer'], was_claimed=False)
class AssignToReviewer(Assign):
    action_form_class = ReviewerChoiceForm
    def update_articles(self):
        super(AssignToReviewer, self).update_articles()
        self.action_qs.update(reviewer=self.action_form.cleaned_data['reviewer'], was_claimed=False)
