from catalog.models import  get_client_ip, Blog
def add_variable_to_context(request):
	return {
        'testme':'test'
    }
def posts(request):
    return {
        'all_posts': Blog.objects.order_by('publish_date'),
    }    