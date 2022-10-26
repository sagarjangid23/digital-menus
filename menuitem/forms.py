from django import forms
from menuitem.models import MenuItem

class MenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image', 'stock', 'available']

    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        for field in (self.fields['name'], self.fields['description'], self.fields['price'], self.fields['image'], self.fields['stock']):
            field.widget.attrs.update({'class': 'shadow appearance-none border rounded w-full py-1.5 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})