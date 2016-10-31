from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Employee
from django.utils import timezone
from .forms import PostForm

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from graphos.renderers import gchart, yui, flot, morris, highcharts, c3js, matplotlib_renderer
from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer,PostSerializer
from .models import University, Student
from .serializers import UniversitySerializer, StudentSerializer


# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def show_employee(request):
    emp = Employee.objects.raw('select id,job_title, count(job_title) as count_job_title from employee group by job_title order by count(job_title) desc,job_title desc limit 2')
    data_source = ModelDataSource(emp, fields=['job_title', 'count_job_title'],)
    # line_chart = highcharts.LineChart(data_source)
    donut_chart = morris.DonutChart(data_source,options={'title': "Sales Growth"})

    avg_list=[]

    avg_list.append(['pay_type','pay'])
    avg_base_pay = Employee.objects.raw('select id,avg(base_pay) as avg_base from employee')
    avg_overtime_pay = Employee.objects.raw('select id,avg(overtime_pay) as avg_overtime from employee')
    avg_other_pay = Employee.objects.raw('select id,avg(other_pay) as avg_other from employee')
    avg_benefits = Employee.objects.raw('select id,avg(benefits) as avg_bene from employee')

    avg_list.append(['avg_base_pay',avg_base_pay[0].avg_base])
    avg_list.append(['avg_overtime_pay' ,avg_overtime_pay[0].avg_overtime])
    avg_list.append(['avg_other_pay' ,avg_other_pay[0].avg_other])
    avg_list.append(['avg_benefits',avg_benefits[0].avg_bene])

    simple_data_source = SimpleDataSource(data=avg_list)
    bar_chart = morris.BarChart(simple_data_source)
    
    return render(request,'blog/show_employee.html',{'donut_chart':donut_chart,'bar_chart':bar_chart})

# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer