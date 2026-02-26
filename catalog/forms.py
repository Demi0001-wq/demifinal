from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product


class ProductForm(forms.ModelForm):
    PROHIBITED_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа', 
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар',
        'casino', 'cryptocurrency', 'crypt', 'stock exchange', 
        'cheap', 'for free', 'deception', 'police', 'radar'
    ]

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price', 'is_published')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Hide is_published for regular users
        if user and not user.has_perm('catalog.can_unpublish_product'):
            if 'is_published' in self.fields:
                del self.fields['is_published']

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        for word in self.PROHIBITED_WORDS:
            if word in cleaned_data.lower():
                raise ValidationError(f'Название не может содержать слово "{word}"')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        for word in self.PROHIBITED_WORDS:
            if word in cleaned_data.lower():
                raise ValidationError(f'Описание не может содержать слово "{word}"')
        return cleaned_data

    def clean_price(self):
        cleaned_data = self.cleaned_data.get('price')
        if cleaned_data < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return cleaned_data
