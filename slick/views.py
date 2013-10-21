import vanilla
from django.db.models import Q
class MessageMixin(object):
  success_message = None
  error_message = None
  def get_error_message(self, form):return self.error_message
  def get_success_message(self, form):return self.success_message
  def form_valid(self, form):
    msg=self.get_success_message(form)
    if msg: messages.success(self.request, msg)
    return super(MessageMixin, self).form_valid(form)

  def form_invalid(self, form):
    error_msg=self.get_error_message(form)
    if error_msg: messages.error(self.request, error_msg)
    return super(MessageMixin, self).form_invalid(form)

class VanillaCreateView(MessageMixin, vanilla.CreateView): pass
class VanillaUpdateView(MessageMixin, vanilla.UpdateView): pass
class VanillaDeleteView(MessageMixin, vanilla.DeleteView): pass
class VanillaFormView(MessageMixin, vanilla.FormView): pass

class ListView(vanilla.ListView):
  search_key = 'q'
  search_on = []
  filter_on = []
  def return_pipe(self, x,y=None):
    if x and y: return x | y
    elif x: return x
    elif y: return y
  def filter(self, queryset):
    # Takes a queryset and returns the queryset filtered
    # If you want to do a custom filter for a certain field,
    # Declare a function: filter_{{fieldname}} that takes a queryset and the value, 
    # does the filter and returns the queryset
    for f in self.filter_on:
      if f in self.request.GET:
        if hasattr(self,'filter_'+f): queryset = getattr(self,'filter_'+f)(queryset, self.request.GET[f])
        else:queryset = queryset.filter(**{f:self.request.GET[f]})
    return queryset
  def search(self, queryset):
    # Takes a queryset and returns the queryset filtered based on search
    # The default search is "field = icontains"
    # If you want to do a custom search on a certain field, there are two ways:
    # 1) Declare a function: search_{{fieldname}} that takes a value and returns a Q()
    #    Example: def search_field(self, value): return Q(field = value)
    # 2) Set search_{{fieldname}} to a string to use as the filter name. 
    #    Example: search_field = "field__icontains"
    if self.search_key in self.request.GET:
      value = self.request.GET[self.search_key]
      query=None
      for field in self.search_on: 
        if hasattr(self,'search_'+field): 
          search=getattr(self,'search_'+field)
          if hasattr(search, '__call__'): query = self.return_pipe(query, search(value))
          elif type(search) == str: query = self.return_pipe(query, Q(**{search:value}))
        else: query = self.return_pipe(query, Q(**{field+"__icontains":value}))
      return queryset.filter(query)
    else: return queryset
  def get_queryset(self):
    queryset = super(ListView, self).get_queryset()
    if self.filter_on: queryset = self.filter(queryset)
    if self.search_on: queryset = self.search(queryset)
    return queryset
  def get_context_data(self, **kwargs):
    context = super(ListView, self).get_context_data(**kwargs)
    print "context = %s" % str(context)
    if self.search_key in self.request.GET: context[self.search_key] = self.request.GET
    print "context = %s" % str(context)
    for filter_key in self.filter_on:
      if filter_key in self.request.GET: context[filter_key] = self.request.GET
    print "context = %s" % str(context)
    return context

