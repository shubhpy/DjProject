from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from django.utils import timezone

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, related_name='user')
#     # photo = FileField(verbose_name=_("Profile Picture"),
#     #                   upload_to=upload_to("main.UserProfile.photo", "profiles"),
#     #                   format="Image", max_length=255, null=True, blank=True)
#     # website = models.URLField(default='', blank=True)
#     # bio = models.TextField(default='', blank=True)
#     # phone = models.CharField(max_length=20, blank=True, default='')
#     # city = models.CharField(max_length=100, default='', blank=True)
#     # country = models.CharField(max_length=100, default='', blank=True)
#     # organization = models.CharField(max_length=100, default='', blank=True)
#     post_list = 


# def create_profile(sender, **kwargs):
#     user = kwargs["instance"]
#     if kwargs["created"]:
#         user_profile = UserProfile(user=user)
#         user_profile.save()

# post_save.connect(create_profile, sender=User)

class Post(models.Model):
	author = models.ForeignKey('auth.user')
	title  = models.CharField(max_length = 200)
	text = models.TextField()
	created_date = models.DateTimeField(default = timezone.now)
	published_date = models.DateTimeField(blank = True,null = True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title


class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    base_pay = models.FloatField(blank=True, null=True)
    overtime_pay = models.FloatField(blank=True, null=True)
    other_pay = models.FloatField(blank=True, null=True)
    benefits = models.FloatField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'employee'


class University(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    university = models.ForeignKey(University, related_name='students')

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)