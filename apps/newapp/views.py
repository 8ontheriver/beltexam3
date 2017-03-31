from django.shortcuts import render, redirect, HttpResponse
from ..logreg.models import User
from .models import Vacation, User
from django.contrib import messages

# Create your views here.

def index(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'user' : User.objects.get(id = request.session['user_id']),
            'peeps' : Vacation.objects.exclude(user = request.session['user_id']).exclude(user_group = request.session['user_id'])
        }
        return render(request, 'newapp/index.html', context)

def details(request, id):
    context = {
        'travel': Vacation.objects.get(id = id),
        'added' : User.objects.filter(group__id = id)
    }
    return render(request, 'newapp/res.html', context)

def newres(request):
	context = {
		'user1' : User.objects.get(id = request.session['user_id']),
	}
    	if not 'user_id' in request.session:
        	messages.error(request, 'Must be logged in to continue!')
        	return redirect('users:index')

    	return render(request, 'newapp/makeres.html', context)

def create(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    if request.method == 'POST':
        response_from_model = Vacation.objects.make(request.POST)

    if response_from_model['status']:
        return redirect('newapp:index')
    else:
        for error in response_from_model['errors']:
            messages.error(request, error)
        return redirect('newapp:newres')

def add(request, id):
	response_from_model = Vacation.objects.add(request.POST, request.session['user_id'], id)
	return redirect('newapp:index')