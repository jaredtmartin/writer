from articles.models import (Article, UserProfile)
from articles.views import (UnavailableArticles, AvailableArticles, AssignedArticles, 
  ClaimedArticles, SubmittedArticles, ApprovedArticles, RejectedArticles, PublishedArticles)
from common import BaseTestCase, InstanceOf, BaseTestCaseAsGuest
from django.core.urlresolvers import reverse

class TestFilterViews(BaseTestCase):
  fixtures = ['fixtures/test_articles_fixture.json']

  def test_unavailable_articles(self):
    response = self.c.get(reverse('unavailable'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    return response
    
  def test_available_articles(self):
    response = self.c.get(reverse('available'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    return response
    
  def test_assigned_articles(self):
    response = self.c.get(reverse('assigned'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    return response
    
  def test_claimed_articles(self):
    response = self.c.get(reverse('claimed'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    return response
    
  def test_submitted_articles(self):
    response = self.c.get(reverse('submitted'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    return response
    
  def test_approved_articles(self):
    response = self.c.get(reverse('approved'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    return response
    
  def test_rejected_articles(self):
    response = self.c.get(reverse('rejected'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    return response
    
  def test_published_articles(self):
    response = self.c.get(reverse('published'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    return response
    
################################################################################
      ####  #####  ###  #   # #####  #### ##### ##### ####   ####
      #   # #     #   # #   # #     #       #   #     #   # #    
      ####  ####  #   # #   # ####   ###    #   ####  ####   ### 
      #   # #     #  ## #   # #         #   #   #     #   #     #
      #   # #####  ####  ###  ##### ####    #   ##### #   # #### 
################################################################################

  def test_unavailable_articles_as_requester(self):  
    response = self.test_unavailable_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      'heading':'Unavailable Articles',
      'is_paginated': False,
      'hidden_columns':['Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':4,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[1,40, 48,49]),
      'object_list':Article.objects.filter(pk__in=[1,40,48,49]),
      'view': InstanceOf(UnavailableArticles),
    })

  def test_available_articles_as_requester(self):  
    response = self.test_available_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      'heading':'Available Articles',
      'is_paginated': False,
      'hidden_columns':['Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':11,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[2,3,4,5,8,9,15,35,36,37,38]),
      'object_list':Article.objects.filter(pk__in=[2,3,4,5,8,9,15,35,36,37,38]),
      'view': InstanceOf(AvailableArticles),
    })

  def test_assigned_articles_as_requester(self):  
    response = self.test_assigned_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (

        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      'heading':'Assigned Articles',
      'is_paginated': False,
      'hidden_columns':['Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':3,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[6,7,11]),
      'object_list':Article.objects.filter(pk__in=[6,7,11]),
      'view': InstanceOf(AssignedArticles),
    })

  def test_claimed_articles_as_requester(self):  
    response = self.test_claimed_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      'heading':'Claimed Articles',
      'is_paginated': False,
      'hidden_columns':['Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':1,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[10]),
      'object_list':Article.objects.filter(pk__in=[10]),
      'view': InstanceOf(ClaimedArticles),
    })

  def test_submitted_articles_as_requester(self):  
    response = self.test_submitted_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      'heading':'Submitted Articles',
      'is_paginated': False,
      'hidden_columns':['Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':7,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[12,13,41,42,44,45,47]),
      'object_list':Article.objects.filter(pk__in=[12,13,41,42,44,45,47]),
      'view': InstanceOf(SubmittedArticles),
    })

  def test_approved_articles_as_requester(self):  
    response = self.test_approved_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      'heading':'Approved Articles',
      'is_paginated': False,
      'hidden_columns':['Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':5,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[14,16, 39, 50,51]),
      'object_list':Article.objects.filter(pk__in=[14,16, 39, 50,51]),
      'view': InstanceOf(ApprovedArticles),
    })

  def test_rejected_articles_as_requester(self):  
    response = self.test_rejected_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      'heading':'Rejected Articles',
      'is_paginated': False,
      'hidden_columns':['Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':4,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[15,40,48,49]),
      'object_list':Article.objects.filter(pk__in=[15,40,48,49]),
      'view': InstanceOf(RejectedArticles),
    })

  def test_published_articles_as_requester(self):  
    response = self.test_published_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 4, False), ('Available', 11, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 5, False), ('Rejected', 4, False), ('Published', 1, False))),
        ('Writers', (('My Writers', 4, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
        ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      'heading':'Published Articles',
      'is_paginated': False,
      'hidden_columns':['Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':1,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[17]),
      'object_list':Article.objects.filter(pk__in=[17]),
      'view': InstanceOf(PublishedArticles),
    })

################################################################################
      #   # ####  ##### ##### ##### ####   ####
      #   # #   #   #     #   #     #   # #    
      # # # ####    #     #   ####  ####   ### 
      # # # #   #   #     #   #     #   #     #
       # #  #   # #####   #   ##### #   # #### 
################################################################################

  def test_unavailable_articles_as_writer(self):  
    self.login(username='MyWriter', password="pass")
    response = self.test_unavailable_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Unavailable Articles',
      'is_paginated': False,
      'hidden_columns':['Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':0,
      'paginator': None,
      'article_list':Article.objects.none(),
      'object_list':Article.objects.none(),
      'view': InstanceOf(UnavailableArticles),
    })

  def test_available_articles_as_writer(self):  
    self.login(username='MyWriter', password="pass")
    response = self.test_available_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Available Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':8,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[2,4,5,8,9,15,37,38]),
      'object_list':Article.objects.filter(pk__in=[2,4,5,8,9,15,37,38]),
      'view': InstanceOf(AvailableArticles),
    })

  def test_assigned_articles_as_writer(self):  
    self.login(username='MyWriter', password="pass")
    response = self.test_assigned_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Assigned Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':2,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[6,7]),
      'object_list':Article.objects.filter(pk__in=[6,7]),
      'view': InstanceOf(AssignedArticles),
    })

  def test_claimed_articles_as_writer(self):  
    self.login(username='MyWriter', password="pass")
    response = self.test_claimed_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Claimed Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':1,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[10]),
      'object_list':Article.objects.filter(pk__in=[10]),
      'view': InstanceOf(ClaimedArticles),
    })

  def test_submitted_articles_as_writer(self):  
    self.login(username='MyWriter', password="pass")
    response = self.test_submitted_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Submitted Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':7,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[12,13,41,42,44,45,47]),
      'object_list':Article.objects.filter(pk__in=[12,13,41,42,44,45,47]),
      'view': InstanceOf(SubmittedArticles),
    })

  def test_approved_articles_as_writer(self):  
    self.login(username='MyWriter', password="pass")
    response = self.test_approved_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Approved Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':4,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[14,16, 50,51]),
      'object_list':Article.objects.filter(pk__in=[14,16, 50,51]),
      'view': InstanceOf(ApprovedArticles),
    })

  def test_rejected_articles_as_writer(self):  
    self.login(username='MyWriter', password="pass")
    response = self.test_rejected_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Rejected Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':1,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[15]),
      'object_list':Article.objects.filter(pk__in=[15]),
      'view': InstanceOf(RejectedArticles),
    })

  def test_published_articles_as_writer(self):  
    self.login(username='MyWriter', password="pass")
    response = self.test_published_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 8, True), ('Assigned', 2, False), ('Claimed', 1, False), ('Submitted', 7, False), ('Approved', 4, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Published Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':0,
      'paginator': None,
      'article_list':Article.objects.none(),
      'object_list':Article.objects.none(),
      'view': InstanceOf(PublishedArticles),
    })

################################################################################
      ####  ##### #   # ##### ##### #   # ##### ####   ####
      #   # #     #   #   #   #     #   # #     #   # #    
      ####  ####   # #    #   ####  # # # ####  ####   ### 
      #   # #      # #    #   #     # # # #     #   #     #
      #   # #####   #   ##### #####  # #  ##### #   # #### 
################################################################################


  def test_unavailable_articles_as_reviewer(self):  
    self.login(username='MyReviewer', password="pass")
    response = self.test_unavailable_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Unavailable Articles',
      'is_paginated': False,
      'hidden_columns':['Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':0,
      'paginator': None,
      'article_list':Article.objects.none(),
      'object_list':Article.objects.none(),
      'view': InstanceOf(UnavailableArticles),
    })

  def test_available_articles_as_reviewer(self):  
    self.login(username='MyReviewer', password="pass")
    response = self.test_available_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Available Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':5,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[41,42,44,45,47]),
      'object_list':Article.objects.filter(pk__in=[41,42,44,45,47]),
      'view': InstanceOf(AvailableArticles),
    })

  def test_assigned_articles_as_reviewer(self):  
    self.login(username='MyReviewer', password="pass")
    response = self.test_assigned_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Assigned Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':0,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[]),
      'object_list':Article.objects.filter(pk__in=[]),
      'view': InstanceOf(AssignedArticles),
    })

  def test_claimed_articles_as_reviewer(self):  
    self.login(username='MyReviewer', password="pass")
    response = self.test_claimed_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Claimed Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':0,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[]),
      'object_list':Article.objects.filter(pk__in=[]),
      'view': InstanceOf(ClaimedArticles),
    })

  def test_submitted_articles_as_reviewer(self):  
    self.login(username='MyReviewer', password="pass")
    response = self.test_submitted_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Submitted Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':0,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[]),
      'object_list':Article.objects.filter(pk__in=[]),
      'view': InstanceOf(SubmittedArticles),
    })

  def test_approved_articles_as_reviewer(self):  
    self.login(username='MyReviewer', password="pass")
    response = self.test_approved_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Approved Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':1,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[50]),
      'object_list':Article.objects.filter(pk__in=[50]),
      'view': InstanceOf(ApprovedArticles),
    })

  def test_rejected_articles_as_reviewer(self):  
    self.login(username='MyReviewer', password="pass")
    response = self.test_rejected_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Rejected Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':1,
      'paginator': None,
      'article_list':Article.objects.filter(pk__in=[48]),
      'object_list':Article.objects.filter(pk__in=[48]),
      'view': InstanceOf(RejectedArticles),
    })

  def test_published_articles_as_reviewer(self):  
    self.login(username='MyReviewer', password="pass")
    response = self.test_published_articles()
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
        ('Articles', (('Unavailable', 0, False), ('Available', 5, True), ('Assigned', 0, False), ('Claimed', 0, False), ('Submitted', 0, False), ('Approved', 1, False), ('Rejected', 1, False), ('Published', 0, False))),
      ),
      'heading':'Published Articles',
      'is_paginated': False,
      'hidden_columns':['Writer','Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':0,
      'paginator': None,
      'article_list':Article.objects.none(),
      'object_list':Article.objects.none(),
      'view': InstanceOf(PublishedArticles),
    })

  def test_user_filtered_available_to_writer(self):
    response = self.c.get(reverse('available'), {'available_to_writer':(10, 11)})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])

class TestFilterViewsAsGuest(BaseTestCaseAsGuest):
  fixtures = ['fixtures/test_articles_fixture.json']
  def test_unavailable_articles(self):
    response = self.c.get(reverse('unavailable'))
  def test_available_articles(self):
    response = self.c.get(reverse('available'))
  def test_assigned_articles(self):
    response = self.c.get(reverse('assigned'))
  def test_claimed_articles(self):
    response = self.c.get(reverse('claimed'))
  def test_submitted_articles(self):
    response = self.c.get(reverse('submitted'))
  def test_approved_articles(self):
    response = self.c.get(reverse('approved'))
  def test_rejected_articles(self):
    response = self.c.get(reverse('rejected'))
  def test_published_articles(self):
    response = self.c.get(reverse('published'))
# Have articles available to two writers and see if they are duplicated in available view
# Test filters from writer and reviewer modes
# Test sombody else's rejected doesnt appear in my view since I'm rewriting it
# Make sure a reviewer can only see articles he rejected / accepted
