class FacebookOutlet(PublishingPluginBase):
    def do_action(self, parent_model):
        raise NotImplemented
    def get_button_url(*args, **kwargs):
        parent_model = kwargs.get('parent_model', None)
        return "http://%s/sharer.php?u=%s&amp;t=%s" % (parent_model.server_domain, body, title)
