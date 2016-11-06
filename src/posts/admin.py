from django.contrib import admin
from .models import Post
class PostModelAdmin(admin.ModelAdmin):
	list_display=['title','updated','timestamp']
	class Meta:
		model = Post


admin.site.register(Post,PostModelAdmin)
# Register your models here.
