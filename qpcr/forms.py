from django import forms

class NewRunForm(forms.Form):
	data = forms.FileField()
	#regex = forms.CharField(max_length=200)
	