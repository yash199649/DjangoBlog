from __future__ import unicode_literals
from django.db.models.signals import pre_save
from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
class Postmanager(models.Manager):
	def active(self,*args,**kwargs):
		return super(Postmanager,self).filter(draft=False).filter(publish__lte=timezone.now())





def upload_location(instance,filename):
	#file_base,extension = filename.split(".")
	return "%s/%s"%(instance.id,filename)



class Post(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	title = models.CharField(max_length=120)
	slug=models.SlugField(unique=True)
	image=models.ImageField(null=True,blank=True,upload_to=upload_location ,height_field="height_field",width_field="width_field")
	height_field=models.IntegerField(default=0)
	width_field=models.IntegerField(default=0)
	content = models.TextField()
	draft=models.BooleanField(default=False)
	publish=models.DateField(auto_now=False,auto_now_add=False)
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	objects=Postmanager()
	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return "/posts/%s" % (self.id)
	def get_markdown(self):
		content=self.content
		return mark_safe(markdown(content))


		#return reverse("detail",kwargs={"id":self.id})
	class Meta:
		ordering=["-timestamp","-updated"]

def create_slug(instance,new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs=Post.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
		new_slug="%s-%s"%(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug



def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)
pre_save.connect(pre_save_post_receiver,sender=Post)