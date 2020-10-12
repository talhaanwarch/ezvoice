from django.db import models

# Create your models here.

MY_CHOICES = (
        ('ur-PK', 'Urdu'),
        ('en-US', 'English'),
        
    )

class Upload(models.Model):
	#pid=models.AutoField(primary_key=True)
	name=models.CharField(max_length=100)
	email=models.EmailField(max_length=50)
	language=models.CharField(max_length=15, choices=MY_CHOICES, default=MY_CHOICES[0][0])

	def __str__(self):
		return self.name

class Text(models.Model):
	texts=models.CharField(max_length=500,null=True,blank=True)
	filename=models.CharField(max_length=100,null=True,blank=True)
	#audio=models.CharField(null=True,blank=True)
	upload_text=models.ForeignKey(Upload, blank=True, null=True, on_delete = models.CASCADE) 