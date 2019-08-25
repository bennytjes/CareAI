from django import forms

class JotFormIDForm(forms.Form):
    principle_1 = forms.CharField(label='Principle 1', max_length=10,required=False)
    principle_2 = forms.CharField(label='Principle 2', max_length=10,required=False)
    principle_3 = forms.CharField(label='Principle 3', max_length=10,required=False)
    principle_4 = forms.CharField(label='Principle 4', max_length=10,required=False)
    principle_5 = forms.CharField(label='Principle 5', max_length=10,required=False)
    principle_6 = forms.CharField(label='Principle 6', max_length=10,required=False)
    principle_7 = forms.CharField(label='Principle 7', max_length=10,required=False)
    principle_8 = forms.CharField(label='Principle 8', max_length=10,required=False)
    principle_9 = forms.CharField(label='Principle 9', max_length=10,required=False)
    principle_10 = forms.CharField(label='Principle 10', max_length=10,required=False)