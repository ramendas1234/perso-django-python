# feeds.py
from django.contrib.syndication.views import Feed
#from django.utils import feedgenerator
from django.urls import reverse
from catalog.models import Blog



class LatestBlogsFeed(Feed):
   title = "Posts for bedjango starter"
   link = "/feeds/"
   description = "Updates on changes and additions to posts published in the starter."
   

   def items(self):
       # return Blog.objects.order_by('publish_date')[:5]
       return Blog.objects.all()

   def item_title(self, item):
       return item.title

   def item_description(self, item):
       return item.description

   def item_link(self, item):
       # return reverse('blog', args=[item.pk])
       return reverse('blog-detail', kwargs = {'pk':item.pk})
       