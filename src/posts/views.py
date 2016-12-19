from urllib import quote_plus
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .models import Post
from django.contrib import messages
from .forms import PostForm
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def posts_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if not request.user.is_authenticated():
		raise Http404
	form = PostForm(request.POST or None , request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user=request.user
		instance.save()
		messages.success(request,"Created Succesfully",extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	
	#if request.method=="POST":
	#	content = request.POST['content']
	#	title = request.POST['title']
	#	print title
	#	Post.objects.create(title=title)
	context={
	"title":"Create",
	"form":form
	}
	return render(request,"post_form.html",context)
def posts_detail(request , id=None):

	instance=get_object_or_404(Post,id=id)
	if  instance.publish>timezone.now().date() or  instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context={
	"title":"Create Blog",
	"instance":instance,

	"share_string":share_string
	}
	return render(request,"post_detail.html",context)

def posts_list(request):
	today=timezone.now().date()
	queryset_list = Post.objects.active()
	if  request.user.is_staff or  request.user.is_superuser:
		queryset_list=Post.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)




			).distinct
	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
	page_request_var='page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	        # If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	        # If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context={
		"queryset":queryset,
		"title":"Blogs",
		"page_request_var":page_request_var,
		"today":today
		}
	return render(request,"post_list.html",context)




def posts_update(request,id):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,id=id)
	form = PostForm(request.POST or None , request.FILES or None ,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Saved")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context={
	"title":"Update Blog",
	"instance":instance,
	"form":form
	}
	return render(request,"post_form.html",context)


	return HttpResponse("<h1> Hey there </h1>")
def posts_delete(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance=get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request,"<a href="">Item</a> Saved",extra_tags='html_safe')
	return redirect('posts:list')
	
