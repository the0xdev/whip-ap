from django.forms import ModelForm
from app.models import Object

class ObjectForm(ModelForm):
    class Meta:
         model = Object
         fields = ["content"]
