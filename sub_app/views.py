from django.shortcuts import render
from .models import *
import base64
from django.http import HttpResponse,HttpResponseRedirect
from .py_templates import sr,symptom_finder
from pydub import AudioSegment
from django.contrib import messages
# Create your views here.
from .forms import uploadForm
import datetime

def text(lang):
	#AudioSegment.converter = r"C:/ffmpeg/bin/ffmpeg.exe"
	#AudioSegment.ffprobe   = r"C:/ffmpeg/bin/ffprobe.exe"
	sound = AudioSegment.from_file("file.oga")
	suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
	filename = "_".join([lang, suffix]) 
	filename='{}.wav'.format(filename)
	sound.export(filename, format="wav")
	tex=sr.takeCommand(filename,lang)
	return tex,filename


def home(request):
	if request.method == 'POST':
		form = uploadForm(request.POST)
		lang=request.POST['language']
		if form.is_valid():
			tex,filename=text(lang)
			if tex is not None:
				form.save()
			
				insert = Text.objects.create(texts=tex,filename=filename,upload_text=Upload.objects.last())
			
				symp=symptom_finder.symp_finder(tex)
				print('symptoms are ', symp)
				return render(request,'search.html',{'text':tex,'doctor_disease':zip(list(symp['doctor']),list(symp['Disease']))})
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
	
