from django import forms
#from marking.models import ICSProjectModel
from kms.models import *

class UploadFileForm(forms.ModelForm):
	class Meta:
		model = File
		fields = "__all__"


# from django import forms
# from marking.models import ICSProjectModel

# class ICSProjectForm(forms.ModelForm):
# 	class Meta:
# 		model = ICSProjectModel
# 		fields = "__all__"