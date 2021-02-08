from django import forms
from .models import ImageUploadModel

class SimpleUploadForm(forms.Form):

    title = forms.CharField(max_length=50)
    image = forms.ImageField()
    # 경로, 이미지 가로&세로 사이즈 저장

    # 파일을 받고 싶을 때는
    # file = forms.FileField()
    # 경로만 저장



class ImageUploadForm(forms.ModelForm):
# Form을 통해 받아들여야 할 데이터가 명시되어 있는 메타 데이터 (DB 테이블을 연결)
    class Meta:
        model = ImageUploadModel
        # Form을 통해 사용자로부터 입력 받으려는 Model Class의 field 리스트
        fields = ('description', 'document', ) # uploaded_at
