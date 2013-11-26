from django.template import Context, Template

class TwitterOutlet(object):
  def get_button_url(self, context=Context()):
    template = Template('<a href="http://twitter.com/home?status={{ article.body|urlencode }}%20{{ article.title|urlencode }}">{{title}}</a>')
    return template.render(context)
