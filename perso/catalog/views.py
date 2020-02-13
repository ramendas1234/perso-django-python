from django.shortcuts import render
from catalog.models import Blog, Category, get_client_ip, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.views.generic.edit import FormMixin
from catalog.forms import CommentForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone



# Create your views here.
def index(request):
	blog_list = Blog.objects.filter().order_by('-publish_date')
	blog_categories = Category.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(blog_list, 9)
	ip_test = get_client_ip(request)
	b_agent = request.META['HTTP_USER_AGENT']
	request.session['user_ip'] = ip_test
	request.session['user_browser'] = b_agent
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		blogs = paginator.page(1)
	except EmptyPage:
		blogs = paginator.page(paginator.num_pages)
	context = {
	'latest_blogs' : blogs,
	'blog_categories' : blog_categories,
	}

	return render(request, 'index.html',context)
class BlogDetailView(FormMixin, generic.DetailView):
	model = Blog
	template_name = 'blog_detail.html'
	form_class = CommentForm
	# success_url = reverse_lazy('blog-detail',args=[str(5)])
	def get_success_url(self):
		return reverse('blog-detail', kwargs={'pk': self.object.id})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		current_post = self.object.id
		#commentator_ip = self.request.session.get('has_comment',0)
		# FETCH Latest Blogs
		context['latest_blogs'] = Blog.objects.filter().exclude(pk=current_post).order_by('-publish_date')[:4]
		#Fetch current blogs comment
		


		if self.request.method == 'POST':
			form = CommentForm(self.request.POST,request=self.request)
			context['form'] = form
			#if commentator_ip == get_client_ip(request)

		else:
			context['form'] = CommentForm(initial={'post': self.object},request=self.request)	
		return context
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = CommentForm(request.POST,request=self.request)
		if form.is_valid():
			#request.session['has_comment'] = get_client_ip(request)
			return self.form_valid(form)
		else:
			return super().form_invalid(form)

		
	def form_valid(self, form):
		#form.comment_date = timezone.now()
		post = form.save(commit=False)
		post.blog_id = self.object.id
		post.comment_date = timezone.now()
		post.save()
		#return super(BlogDetailView, self).form_valid(form)
		return super().form_valid(form)
	def form_invalid(self, form):
		#return super().form_invalid(form)
		return form.errors

class ArticleMonthArchiveView(generic.dates.MonthArchiveView):
	queryset = Blog.objects.all()
	date_field = "publish_date"
	allow_future = True
	context_object_name = 'latest_blogs'
	
# Class Use for Blog Listing 

class BlogListView(generic.ListView):
	model = Blog
	template_name = 'catalog/blog_archive_month.html'
	context_object_name = 'latest_blogs'

#class CategoriesListView(generic.ListView):

def CategoriesList(request, pk):
	blog_list = Blog.objects.all().filter(category=pk)
	catg = Category.objects.get(pk = pk)
	page = request.GET.get('page', 1)
	paginator = Paginator(blog_list, 9)
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		blogs = paginator.page(1)
	except EmptyPage:
		blogs = paginator.page(paginator.num_pages)
	context = {
	'latest_blogs' : blogs,
	'category_name' : catg
	}
	return render(request, 'catalog/blog_archive_month.html',context) 
class LatestBlogsFeed():
        title = "Posts for bedjango starter"	