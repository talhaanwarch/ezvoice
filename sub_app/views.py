from django.shortcuts import render
from .models import *
import base64
from django.http import HttpResponse,HttpResponseRedirect
from .py_templates import sr
from pydub import AudioSegment
from django.contrib import messages
# Create your views here.
from .forms import uploadForm
def text():
	#AudioSegment.converter = r"C:/ffmpeg/bin/ffmpeg.exe"
	#AudioSegment.ffprobe   = r"C:/ffmpeg/bin/ffprobe.exe"
	print('file.oga loaded')
	sound = AudioSegment.from_file("file.oga")
	print('file.oga loaded 1')
	sound.export("filew.wav", format="wav")
	print('pydub exported')
	tex=sr.takeCommand('filew.wav')
	print(tex)
	return tex


def home(request):
	if request.method == 'POST':
		form = uploadForm(request.POST)
		if form.is_valid():
			tex=text()
			if tex is not None:
				form.save()
			
				print(tex)
				insert = Text.objects.create(texts=tex,upload_text=Upload.objects.last())
			

				return render(request,'search.html',{'text':tex})
				#messages.success(request,'voice saved')
			else:

				return render(request,'search.html',{'text':'Please speak again'})
	else:
		form = uploadForm()

	return render(request,'home.html',{'load':form})





def search(request):
	if request.method=='POST':
		query=request.POST.get('Search')
		# data=Upload.objects.filter(name__icontains=query)
		# data1=Text.objects.filter(upload_text__in=data)
		#data=Upload.objects.filter(name__icontains=query).prefetch_related('text_set')
		data=Text.objects.filter(upload_text__name__icontains=query)

		print(data)
		return render(request,'search.html',{'query_key':data})
	else:
		pass
	return render(request,'search.html',{'query_key':'Search Value'})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_audio(request):
	print('upload_audio')
	if request.is_ajax():
		
		req=request.POST.get('data')
		d=req.split(",")[1]
		print("Yes, AJAX!")
		#print(request.body)
		f = open('./file.oga', 'wb')
		
		f.write(base64.b64decode(d))
		#f.write(request.body)
		f.close()
	return HttpResponse('audio received')
	
