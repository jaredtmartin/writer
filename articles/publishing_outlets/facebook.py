from django.template import Context, loader

class FacebookOutlet(object):
    def do_action(self, parent_model):
        raise NotImplemented
    def get_button_url(self, context=Context()):
        template = loader.get_template('articles/facebook_button.html')
        return template.render(context)
