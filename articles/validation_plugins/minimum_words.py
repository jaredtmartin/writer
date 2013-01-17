from articles.models import ValidationProvider
class MinimumWordsValidator(ValidationProvider):
    title = "Minimum Words"
    name = 'minimum_words'
    description = u"Requires that the article body contatins a certain minimum number of words"
    
    def is_valid(self, article):
        return len(article.body)>0

class NotEmptyValidator(ValidationProvider):
    title = "Not Empty"
    name = 'not_empty'
    description = u"Requires that the article body not be empty"
    
    def is_valid(self, article):
        return len(article.body)>0
