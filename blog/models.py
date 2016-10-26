from __future__ import unicode_literals


from django.db import models

# Create your models here.
from django.utils import timezone

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