from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	
	def register(self, postData):
		errors = []

		if len(postData['name']) < 3:
			errors.append('Name must be at least 3 characters long!')
		if not len(postData['username']):
			errors.append('Username is required!')
		if len(postData['username']) < 3:
			errors.append('Username must be at least 3 characters long!')
		if len(postData['password']) < 8:
			errors.append('Password must be at least 8 characters long!')
		if not postData['password'] == postData['confirm_password']:
			errors.append('Paswords must match!')

		user = self.filter(username = postData['username'])

		if user:
			errors.append('Username must be unique!')

		modelResponse = {}

		if errors:
			modelResponse['status'] = False
			modelResponse['errors'] = errors

		else:
			hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

			user = self.create(name = postData['name'], username = postData['username'], password = hashed_password)

			modelResponse['status'] = True
			modelResponse['user'] = user

		return modelResponse


	def login(self, postData):
		
		user = self.filter(username = postData['username'])

		modelResponse = {}

		if user:
			if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):

				modelResponse['status'] = True
				modelResponse['user'] = user[0]

			else:
				modelResponse['status'] = False
				modelResponse['error'] = 'Invalid username/password combination!'

		else:
			modelResponse['status'] = False
			modelResponse['error'] = 'Invalid username!'


		return modelResponse

class User(models.Model):
	name = models.CharField(max_length=45)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()