from articles.models import (Article)
from articles.views import (AvailableArticles)
from common import BaseTestCase, InstanceOf

class TestArticles(BaseTestCase):
  fixtures = ['fixtures/test_articles_fixture.json']
  def test_avilable_articles_list(self):
    """ Just a simple run through"""
    response = self.c.get('/articles/available/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.template_name, ['articles/article_list.html'])
    self.assertContext(response, {
      'all_columns':['Project', 'Keywords', 'Writer', 'Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'sidebar_links': (
          ('Articles', (('Unavailable', 1, False), ('Available', 7, False), ('Assigned', 3, False), ('Claimed', 1, False), ('Submitted', 2, False), ('Approved', 2, False), ('Rejected', 1, False), ('Published', 1, False))), 
          ('Writers', (('My Writers', 1, False), ('Writers Pending', 1, False), ('Writers Avail.', 2, True), ('Writer Groups', 1, True))), 
          ('Reviewers', (('My Reviewers', 1, False), ('Reviewers Pending', 1, False), ('Reviewers Avail.', 2, True), ('Reviewer Groups', 1, True)))
        ),
      # 'reviewer_filter_counts':{'Reviewers Pending': (1, False), 'Reviewers Avail.': (2, True), 'Reviewer Groups': (1, True), 'My Reviewers': (1, False)},
      'heading':'Available Articles',
      'is_paginated': False,
      # 'article_filter_counts':{'Available': (7, False), 'Assigned': (3, False), 'Unavailable': (1, False), 'Published': (1, False), 'Claimed': (1, False), 'Approved': (2, False), 'Submitted': (2, False), 'Rejected': (1, False)},
      'hidden_columns':['Reviewer', 'Status', 'Category', 'Length', 'Priority', 'Tags'],
      'page_obj': None,
      'all_items_count':7,
      'paginator': None,
      # 'writer_filter_counts':{'My Writers': (1, False), 'Writers Pending': (1, False), 'Writers Avail.': (2, True), 'Writer Groups': (1, True)},
      'article_list':Article.objects.filter(pk__in=[2,3,4,5,8,9,15]),
      'object_list':Article.objects.filter(pk__in=[2,3,4,5,8,9,15]),
      'view': InstanceOf(AvailableArticles),
    })
