from django import forms
from eproperty.models import Property, PropertyImages

# Property Form
class PropertyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Property
        exclude = {'user'}
        widget = {
            'propertyConstructionDate': forms.DateInput(attrs={'placeholder':'(YYYY-MM-DD)'}),
        }
        fields = "__all__"

#Property Image Form
class PropertyImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PropertyImageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = PropertyImages
        fields = ['propertyImage']