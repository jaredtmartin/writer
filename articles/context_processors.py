from django.contrib.auth.forms import AuthenticationForm

def login_form(request):
	if not request.user.is_authenticated(): return {login_form:AuthenticationForm()}
	else: return {}