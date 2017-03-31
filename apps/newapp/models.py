from __future__ import unicode_literals
from django.db import models
from ..logreg.models import User
import time
import datetime

# Create your models here.
class UserManager(models.Manager):

	def make(self, postData):
		response_to_views = {}
		errors = []

		if not len(postData['name']):
			errors.append('Must enter a destination!')

		if not len(postData['descript']):
			errors.append('Must enter a description!')

		if not postData['start_date']:
			errors.append('Start date required!')

		if not postData['end_date']:
			errors.append('End date required!')

		else:
			start_date = datetime.datetime.strptime(postData['start_date'],'%Y-%m-%d')
			end_date = datetime.datetime.strptime(postData['end_date'],'%Y-%m-%d')

			if start_date > end_date:
				errors.append('End date must be after start date!')

		if errors:
			print errors
			response_to_views['status'] = False
			response_to_views['errors'] = errors
		else:

			user = User.objects.get(id = postData['user_id'])

			flight = self.create(name = postData['name'], descript = postData['descript'], start_date = postData['start_date'], end_date = postData['end_date'], user = user)
			vacation = self.get(name = postData['name'], descript = postData['descript'], start_date = postData['start_date'], end_date = postData['end_date'], user = user)

			vacation.user_group.add(user)

			response_to_views['status'] = True
			response_to_views['trip'] = flight

		return response_to_views

	def add(self, postData, user_id, id):
		traveler = User.objects.get(id=user_id)
		vacation = Vacation.objects.get(id=id)
		vacation.user_group.add(traveler)


class Vacation(models.Model):
    name = models.CharField(max_length = 255)
    descript = models.CharField(max_length = 255)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name="traveler")
    user_group = models.ManyToManyField(User, related_name = "group")

    objects = UserManager()

		