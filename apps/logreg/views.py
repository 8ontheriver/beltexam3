from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, 'logreg/index.html')

def register(request):
	print request.POST

	response_from_models = User.objects.register(request.POST)

	if response_from_models['status']:
		request.session['user_id'] = response_from_models['user'].id
		return redirect('newapp:index')

	else:
		print response_from_models['errors']
		for error in response_from_models['errors']:
			messages.error(request, error)
			print error
		return redirect('users:index')

def login(request):
	print request.POST

	response_from_models = User.objects.login(request.POST)

	if response_from_models['status']:
		request.session['user_id'] = response_from_models['user'].id
		request.session['name'] = response_from_models['user'].name

		return redirect('newapp:index')

	else:
		print response_from_models['error']
		messages.error(request, response_from_models['error'])
		return redirect('users:index')


def success(request):
	if not 'user_id' in request.session:
		messages.error(request, 'Must be logged in!')
		return redirect('users:index')

	return render(request, 'logreg/success.html')

def logout(request):
	request.session.clear()
	return redirect('users:index')

	