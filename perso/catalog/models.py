from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django import forms
from django.utils import timezone
from django.urls import reverse

# Create your models here.

#Create blogs 
class Blog(models.Model):
	title = models.CharField(blank=False,help_text = 'Enter blog title', max_length=200)
	description = models.TextField(blank=False,help_text = 'Give blog description')
	blog_image = models.ImageField(blank=False, upload_to="uploads/")
	category = models.ManyToManyField('Category', help_text="Select a blog category")
	publish_date = models.DateField(default=timezone.now())

	def get_category_name(self):
		return ', '.join([category.name for category in self.category.all()[:3]])
	def get_absolute_url(self):
		"""Returns the url to access a particular book instance."""
		return reverse('blog-detail', args=[str(self.id)])
	def __str__(self):
		return self.title

class Category(models.Model):
	name = models.CharField(blank=False,help_text = 'Enter blog category name', max_length=200)
	category_image = models.ImageField(blank=False, upload_to="uploads/")
	def __str__(self):
		return self.name
class Comments(models.Model):
	name = models.CharField(blank=False, max_length=20)
	description = models.TextField(blank=False)
	blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
	comment_date = models.DateField()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip		