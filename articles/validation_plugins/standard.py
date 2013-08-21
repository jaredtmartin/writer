from articles.models import ValidationProvider
from django.contrib import messages
class MinMaxWordsValidator(ValidationProvider):
    title = "Minimum and Maximum Words"
    description = u"Requires that the article body contatins th"
    
    def count_words(self, text):
        print "len(text.split()) = %s" % str(len(text.split()))
        return len(text.split()) + 1
    def is_valid(self, article, request):
        text = self.strip_tags(article.body)
        num_words = self.count_words(text)
        if article.maximum and num_words > article.maximum: 
            messages.error(request, "The article is too long, it should have less than %s \
                words" % article.maximum)
            return False
        if num_words < article.minimum:
            messages.error(request, "The article is too short. It must have at least %s \
                words." % article.minimum)
            return False
        return True
class NotEmptyValidator(ValidationProvider):
    title = "Not Empty"
    description = u"Requires that the article body not be empty"
    
    def is_valid(self, article, request):
        if len(article.body) == 0:
            messages.error(request, "The article has no body. Please type an article before \
                submitting")
            return False
        return True

class ContainsKeywordsValidator(ValidationProvider):
    title = "Contains Keywords"
    description = u"Requires that the article body contains the keywords the specified number of \
        times."
    
    def is_valid(self, article, request):
        text = self.strip_tags(article.body)
        for keyword in article.keyword_set.all():
            if not text.count(keyword.keyword) >= keyword.times: 
                messages.error(request, "The article does not contain all of the required \
                    keywords or does not have the specified number of the keywords. The keyword \
                    '%s' should appear %i time(s) but it only appears %i time(s)." % \
                    (keyword.keyword, keyword.times, text.count(keyword.keyword)))
                return False
        return True