from django.forms import ModelForm
from .models import Upload
#https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
#https://docs.djangoproject.com/en/3.1/topics/forms/
class uploadForm(ModelForm):
	class Meta:
		model = Upload
		#fields = ['name', 'gender', 'phone', 'email','file']
		fields= '__all__'
