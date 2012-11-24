from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from models import Form, Element, Value, Result
from forms import make_form, make_form_class, FormModelForm, ElementInline, ElementForm, BareFormModelForm
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
import csv
from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.sites.models import Site
from django.conf import settings
import base64
import json
import hmac
import hashlib

from django_facebook.decorators import canvas_only, facebook_required

def base64_url_decode(inp):
    inp = inp.replace('-','+').replace('_','/')
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.decodestring(inp)


def parse_signed_request(signed_request='a.a', secret=settings.FACEBOOK_APP_SECRET):
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        print('Unknown algorithm')
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        print('valid signed request received..')
        return data
class FacebookLoginMixin(object):
    def facebook_login_redirect(self, request):
            return_uri="http://"+request.get_host()+request.get_full_path()
            request.session['return_uri']=return_uri
#            return_uri = 'http://ec2-23-23-250-102.compute-1.amazonaws.com/forms/1-x/'
#                         'http://ec2-23-23-250-102.compute-1.amazonaws.com/forms/1-x/'
            redirect_url = 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&state=%s' % (settings.FACEBOOK_APP_ID, return_uri, '777')
#            print "are we here?"
            print "redirect_url: " + str(redirect_url) 
            return redirect(redirect_url)
    def get(self, request, *args, **kwargs):
        try: 
            print "request.POST.get('signed_request'): " + str(request.POST.get('signed_request')) 
            if request.facebook: 
                print "im here"
                self.object = self.get_object()
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)
            else: 
                print "im here"
                print "request.get_host(): " + str(request.get_host()) 
                print "request.get_full_path(): " + str(request.get_full_path()) 
                return self.facebook_login_redirect(request)
        except AttributeError: 
            return self.facebook_login_redirect(request)
        
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

class FormGetView(FacebookLoginMixin, DetailView, FormMixin):
    model = Form
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
#        context['facebook']=self.request.facebook
        context['site']=Site.objects.get_current()
        context['me'] = self.request.facebook.graph.get_object('me')
        print "self.request: " + str(self.request) 
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
#    @method_decorator(facebook_required)
#    def dispatch(self, *args, **kwargs):
#        return super(FormGetView, self).dispatch(*args, **kwargs)

class FormView(FormGetView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class CreateFormView(CreateWithInlinesView):
    model = Form
    form_class = FormModelForm
    inlines = [ElementInline]
    def get_form_kwargs(self):
        kwargs=super(CreateFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    def get_context_data(self, **kwargs):
        context = super(CreateFormView, self).get_context_data(**kwargs)
        context.update({'sample_elements': get_sample_elements()})
        return context

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
        return context
