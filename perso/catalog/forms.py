from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from catalog.models import Comments, get_client_ip



# CREATE COMMENT forms
class CommentForm(forms.ModelForm):

	ip = None
	def __init__(self, *args, request=None, **kwargs):
 		super(CommentForm, self).__init__(*args, **kwargs)
 		self.request = request  # perhaps you want to set the request in the Form
 		
 		
 		if self.request is not None:
 			self.ip = self.request.session.get('has_comment',0)
 		

	class Meta:
		model = Comments
		fields = ('name', 'description',)
		labels = {
		'name': _('Commentor Name'),
		'description' : _('Comments')
		}
		error_messages = {
		'name': {
		'max_length': _("This writer's name is too long."),
		'required': _("Hey baby enter your name")
		},
		}
	# IF YOU NEED TO ADD CUSTOM EXTRA VALIDATION THEN USE clean Function	
	def clean(self):
		data = self.cleaned_data

		# Here Is ip validation if visitor has already comment 
		# if self.ip is not None and self.ip == get_client_ip(self.request):
		# 	raise forms.ValidationError('You have already Comments')

		
		# if data.get("name") is None:
		# 	raise forms.ValidationError('Enter Your name')
		# elif len(data['name']) > 2:
		# 	raise forms.ValidationError('Name field is too long')
	
