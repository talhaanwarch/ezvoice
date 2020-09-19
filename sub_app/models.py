from django.db import models

# Create your models here.
class Upload(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField(max_length=50)

	def __str__(self):
		return self.name

class Text(models.Model):
	texts=models.CharField(max_length=500,null=True,blank=True)
	#audio=models.CharField(null=True,blank=True)
	upload_text=models.ForeignKey(Upload, blank=True, null=True, on_delete = models.CASCADE) 