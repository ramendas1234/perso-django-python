from django.contrib import admin
from .models import Blog, Category

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
	list_display = ('title','get_category_name','publish_date')
admin.site.register(Blog, BlogAdmin)

admin.site.register(Category)
