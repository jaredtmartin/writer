class PublishingPluginBase(object):
    def do_action(self, parent_model):
        raise NotImplemented
    def get_button_url(*args, **kwargs):
        raise NotImplemented
