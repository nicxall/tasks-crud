from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .models import TaskModel
from django.views.generic import UpdateView, TemplateView

from django.http import HttpResponse
#Import file verification methods http
from .validations import render_template
# Create your views here.

class TemplateHome(TemplateView):
	template_name = "home.html"
	user = User.username

	def get(self, request):
		if request.user.is_authenticated:
			return render(request, self.template_name)
		else:
			return redirect('signin')

class SigninUser(View):
	template_name = "signin.html"
	def get(self, request):
		return render(request, self.template_name)
	def post(self, request):
		try:
			validation_data = authenticate(
				username = request.POST['username'],
				password = request.POST['password']
			)
			if validation_data is None:
				print("No se pudo iniciar sesion")
				return render(request, 'signin.html')
			login(request, validation_data)
			print('Fue todo un exito')
			return redirect('home')
		except User.DoesNotExist:
			return HtppResponse("Lo sentimos sus datos no existen en la base de datos")

class Signup(View):
	template_name = "signup.html"
	def get(self, request):
		return render(request, self.template_name)
	def post(self, request):
		if request.POST['password1'] == request.POST['password2']:
			try:
				DataCreate = User.objects.create_user(
					username = request.POST['username'],
					password = request.POST['password1']
				)
				DataCreate.backend = 'django.contrib.auth.backends.ModelBackend'
				DataCreate.save()
				login(request, DataCreate)
				return redirect('home')
			except IntegrityError:
				return redirect('signup')

def SessionCloseUser(request):
	logout(request)
	return redirect('signin')