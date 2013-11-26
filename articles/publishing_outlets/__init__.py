class PublishingPluginBase(object):
  settings=[]
  def do_action(self):
    raise NotImplemented
  def get_button_url(*args, **kwargs):
    raise NotImplemented
