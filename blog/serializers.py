from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Post, Employee
from .models import University, Student

 # Serializers define the API representation.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('url', 'username','email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url','author','title', 'text', 'created_date','published_date')

class UniversitySerializer(serializers.ModelSerializer):
	students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = University
		fields = ('id','name','students')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','first_name','last_name','university')
