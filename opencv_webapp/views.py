from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from opencv_webapp.forms import SimpleUploadForm, ImageUploadForm
from opencv_webapp.cv_functions import cv_detect_face


# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})

def simple_upload(request):
    if request.method == 'POST': # POST
        # print(request.POST) : <QueryDict: {'csrfmiddlewaretoken': [‘~~~’], 'title': ['upload_1']}>
        # print(request.FILES) : <MultiValueDict: {'image': [<InMemoryUploadedFile: ses.jpg (image/jpeg)>]}>

        form = SimpleUploadForm(request.POST, request.FILES) # filled form

        if form.is_valid(): # validation check
            myfile = request.FILES['image']

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile) # myfile.name -> img.jpg
            uploaded_file_url = fs.url(filename)

            context = {'form':form, 'uploaded_file_url':uploaded_file_url}
            return render(request, 'opencv_webapp/simple_upload.html', context)

    else: # GET
        form = SimpleUploadForm() # empty form
        context = {'form':form}
        return render(request, 'opencv_webapp/simple_upload.html', context)


def detect_face(request):

    if request.method == 'POST' :
        form = ImageUploadForm(request.POST, request.FILES) # filled form

        if form.is_valid():
            # Form에 채워진 데이터를 DB에 실제로 저장하기 전에 변경하거나 추가로 다른 데이터를 추가할 수 있음
            post = form.save(commit=False) # post는 DB 하나의 row
            post.save() # DB에 실제로 Form 객체('form')에 채워져 있는 데이터를 저장
	        # post는 save() 후 DB에 저장된 ImageUploadModel 클래스 객체 자체를 갖고 있게 됨 (record 1건에 해당)

            imageURL = settings.MEDIA_URL + form.instance.document.name
            # '/media/' + 'img.jpg'
	        # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당

            # print(form.instance, form.instance.document.name, form.instance.document.url)
            # form.instance                 -> ImageUploadModel object (1)
            # form.instance.document.name   -> images/2021/02/08/ses.jpg
            # form.instance.document.url    -> /media/images/2021/02/08/ses.jpg

            # 얼굴 검출
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)

            context = {'form': form, 'post': post}

            return render(request, 'opencv_webapp/detect_face.html', context)

    else:
         form = ImageUploadForm() # empty form
         context = {'form': form}

         return render(request, 'opencv_webapp/detect_face.html', context)








#
