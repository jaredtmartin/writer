from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from models import Form, Element, Value, Result, Theme
from forms import make_form, make_form_class, ElementInline, ElementForm, BareFormModelForm, NameAndThemeForm, ShareForm
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
import csv
from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse
import facebook
#import base64
#import json
#import hmac
#import hashlib

#from django_facebook.decorators import canvas_only, facebook_required

#class RequireFacebookLoginMixin(object):
#    def facebook_login_redirect(self, request):
#            return_uri="http://"+request.get_host()+request.get_full_path()
#            request.session['return_uri']=return_uri
#            redirect_url = 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&state=%s' % (settings.FACEBOOK_APP_ID, return_uri, '777')
#            return redirect(redirect_url)
#    def get(self, request, *args, **kwargs):
#        print "request: " + str(request) 
#        print "request.facebook: " + str(request.facebook) 
#        if request.facebook: 
#            self.object = self.get_object()
#            context = self.get_context_data(object=self.object)
#            print "got this far"
#            return self.render_to_response(context)
#        else: 
#            print "now im here"
#            return self.facebook_login_redirect(request)

def facebook_required(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if not request.facebook:
                return_uri="http://"+request.get_host()+request.get_full_path()
                request.session['return_uri']=return_uri
                redirect_url = 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&state=%s&scope=%s' % (settings.FACEBOOK_APP_ID, return_uri, '777',",".join(settings.FACEBOOK_SCOPE))
                return redirect(redirect_url)
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)

class KeyMixin(object):
    def get_queryset(self):
        from django.db.models import Q
        qs=super(KeyMixin, self).get_queryset()
        if not self.request.user.is_staff:
            user_id=getattr(self.request.user, "pk", None)
            key=self.request.GET.get('key','xxx')
            qs=qs.filter(Q(created_by_id=user_id)|Q(key=key))
        return qs

class OwnerMixin(object):
    def get_queryset(self):
        from django.db.models import Q
        qs=super(OwnerMixin, self).get_queryset()
        if not self.request.user.is_staff:
            user_id=getattr(self.request.user, "pk", None)
            qs=qs.filter(created_by_id=user_id)
        return qs
        
def get_sample_elements():
    return [
        ElementForm(instance=Element(klass=Element.TEXTBOX)),
        ElementForm(instance=Element(klass=Element.TEXT)),
        ElementForm(instance=Element(klass=Element.IMAGE)),
        ElementForm(instance=Element(klass=Element.IMAGELEFT)),
        ElementForm(instance=Element(klass=Element.IMAGERIGHT)),
        ElementForm(instance=Element(klass=Element.PASSWORD)),
        ElementForm(instance=Element(klass=Element.TEXTAREA)),
        ElementForm(instance=Element(klass=Element.DROPDOWN)),
        ElementForm(instance=Element(klass=Element.RADIO)),
        ElementForm(instance=Element(klass=Element.URL)),
        ElementForm(instance=Element(klass=Element.COUNTRY)),
        ElementForm(instance=Element(klass=Element.EMAIL)),
    ]
class FormList(ListView):
    model = Form
    
class ThankYou(DetailView):
    model = Form
    template_name="forms/thankyou.html"

class FacebookView(DetailView):
    model = Form
    template_name="forms/facebook.html"
    def get_context_data(self, **kwargs):
        context = super(FacebookView, self).get_context_data(**kwargs)
        context['site']=Site.objects.get_current()
        return context

class ExportCSV(OwnerMixin, DetailView):
    model = Form
    def get_results_headings(self):
        values=[]
        results=self.object.results.all()
        if results: 
            values=results[0].values.all()
        return [v.element.name for v in values]
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="form_export.csv"'

        results=self.object.results.all()
        if results: 
            writer = csv.writer(response)
            sample_values=results[0].values.all()
            writer.writerow([v.element.name for v in sample_values])
            for result in results:
                writer.writerow([v.value for v in result.values.all()])
        return response

class FormGetView(DetailView, FormMixin):
    model = Form
    template_name = 'forms/form_show.html'
    success_url = '/forms/'
    context_object_name = 'object'
    def get_context_data(self, **kwargs):
        context = super(FormGetView, self).get_context_data(**kwargs)
        if not 'form' in context or context['form'].__class__ is Form: 
            context['form'] = make_form(self.object)
        context['object'] = self.object
        user=self.request.user
        user.can_edit=(user==self.object.created_by or user.is_staff)
        context['user']=user
        context['site']=Site.objects.get_current()
        try: context['me'] = self.request.facebook.graph.get_object('me')
        except AttributeError:pass 
        return context
            
    def get_form_class(self):
        return make_form_class(self.object)
    def get_success_url(self):
        return self.object.success_url
    def form_valid(self, form):
        result=Result.objects.create(form=self.object)  
        for e in self.object.elements.exclude(klass__startswith='I').exclude(klass="TX").exclude(klass="HD"):
            c=form.cleaned_data
            Value.objects.create(element=e, value=form.cleaned_data[e.name], result=result)
        return super(FormGetView, self).form_valid(form)

class FormView(FormGetView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
#class CreateFormView(CreateWithInlinesView):
#    model = Form
#    form_class = FormModelForm
#    inlines = [ElementInline]
#    def get_form_kwargs(self):
#        kwargs=super(CreateFormView, self).get_form_kwargs()
#        kwargs.update({'request': self.request})
#        return kwargs
#    def get_context_data(self, **kwargs):
#        context = super(CreateFormView, self).get_context_data(**kwargs)
#        context.update({'sample_elements': get_sample_elements()})
#        return context

class UpdateFormView(OwnerMixin, UpdateWithInlinesView):
    model = Form
    form_class = BareFormModelForm
    context_object_name = 'object'
    inlines = [ElementInline]
#    def get_form_kwargs(self):
#        kwargs=super(UpdateFormView, self).get_form_kwargs()
#        kwargs.update({'request': self.request})
#        return kwargs
    def get_context_data(self, **kwargs):
        context = super(UpdateFormView, self).get_context_data(**kwargs)
        context.update({'sample_elements': get_sample_elements()})
        user = facebook.get_user_from_cookie(self.request.COOKIES,settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
        print "user: " + str(user) 
        return context
    #@method_decorator(facebook_required)
    def dispatch(self, request, *args, **kwargs):
        print "request: " + str(request) 
        return super(UpdateFormView, self).dispatch(request, *args, **kwargs)

class CreateFormAndTheme(OwnerMixin, CreateView):
    model = Form
    form_class = NameAndThemeForm
    context_object_name = 'object'
    template_name='forms/form_theme.html'
    def get_success_url(self):return self.object.get_edit_url()
    def get_context_data(self, **kwargs):
        context = super(CreateFormAndTheme, self).get_context_data(**kwargs)
        context['themes']=Theme.objects.all()
        try: context['me'] = self.request.facebook.graph.get_object('me')
        except AttributeError:pass 
        return context
    def get_form_kwargs(self):
        kwargs=super(CreateFormAndTheme, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
   # @method_decorator(facebook_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateFormAndTheme, self).dispatch(request, *args, **kwargs)
    
class UpdateFormAndTheme(OwnerMixin, UpdateView):
    model = Form
    form_class = NameAndThemeForm
    context_object_name = 'object'
    template_name='forms/form_theme.html'
    def get_success_url(self):return self.object.get_edit_url()
    def get_context_data(self, **kwargs):
        context = super(UpdateFormAndTheme, self).get_context_data(**kwargs)
        context['themes']=Theme.objects.all()
        try: context['me'] = self.request.facebook.graph.get_object('me')
        except AttributeError:pass 
        return context
    #@method_decorator(facebook_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateFormAndTheme, self).dispatch(request, *args, **kwargs)
        
class UpdateFormShare(OwnerMixin, UpdateView):
    model = Form
    form_class = ShareForm
    context_object_name = 'object'
    template_name='forms/form_share.html'
    def get_pages(self):
        pages=[]
        graph=self.request.facebook.graph
        for account in graph.request('/me/accounts/')['data']:
            if not account['category'] == 'Application':
                pages.append(account['name'])
        return pages
    def get_context_data(self, **kwargs):
        context = super(UpdateFormShare, self).get_context_data(**kwargs)
        try: 
            print "I'm here"
            print "self.request.user: " + str(self.request.user) 
            context['me'] = self.request.facebook.graph.get_object('me')
            print "context['me']: " + str(context['me']) 
            context['pages'] = self.get_pages()
            print "context: " + str(context) 
            context['site']=Site.objects.get_current()
        except AttributeError as e:
            print "there was an error:%s" % str(e)
        return context
    @method_decorator(facebook_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateFormShare, self).dispatch(request, *args, **kwargs)
class ConfirmFacebookAddition(DetailView):
    model = Form
    template_name = 'forms/facebook-confirmed.html'
    def get_context_data(self, **kwargs):
        context = super(ConfirmFacebookAddition, self).get_context_data(**kwargs)
        print "self.request: " + str(self.request) 
        return context
