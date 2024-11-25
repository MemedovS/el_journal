from django import forms
from django.forms.models import modelformset_factory

from .models import Student, Contact, User


class UserCreateForm(forms.ModelForm):
    """Форма создания нового пользователя."""
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'middle_name',
                  'birth_date', 'sex', 'photo', 'description']
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'Abunəci adı'}),
                   'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
                   'password': forms.PasswordInput(attrs={'placeholder': 'Şifrə'}),
                   'first_name': forms.TextInput(attrs={'placeholder': 'Ad'}),
                   'last_name': forms.TextInput(attrs={'placeholder': 'SoyAd'}),
                   'middle_name': forms.TextInput(attrs={'placeholder': 'AtaAdı'}),
                   'birth_date': forms.DateInput(attrs={'placeholder': 'Doğum tarixi', 'type': 'date'}),
                   'sex': forms.Select(attrs={'placeholder': 'cinsi'}),
                   'photo': forms.FileInput(attrs={'class': 'input-file'}),
                   'description': forms.Textarea(attrs={'placeholder': 'Xarakterik', 'rows': 5, 'cols': 30}),
                   }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Форма для обновления данных пользователя."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name',
                  'sex', 'birth_date', 'photo', 'description']
        widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Ad'}),
                   'last_name': forms.TextInput(attrs={'placeholder': 'SoyAd'}),
                   'middle_name': forms.TextInput(attrs={'placeholder': 'AtaAdı'}),
                   'birth_date': forms.DateInput(attrs={'type': 'date', 'data-date-format': 'yyyy-mm-dd'},
                                                 format=('%Y-%m-%d')),
                   'sex': forms.Select(attrs={'placeholder': 'cinsi'}),
                   'photo': forms.FileInput(attrs={'class': 'input-file'}),
                   'description': forms.Textarea(attrs={'placeholder': 'Xarakterik', 'rows': 5, 'cols': 40}),
                   }


class StudentForm(forms.ModelForm):
    """Форма связанная с пользовательской формой, информация о студенте."""
    class Meta:
        model = Student
        fields = ('group',)
        widgets = {'group': forms.Select()}


class ContactForm(forms.ModelForm):
    """Форма связанная с пользовательской формой, контактные данные."""
    class Meta:
        model = Contact
        fields = ['phone', 'email']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Əsas telefon nömrəsi'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Elektron poçt ünvanı'}),
        }

ContactFormSet = modelformset_factory(Contact, form=ContactForm, max_num=1, extra=1)
StudentFormSet = modelformset_factory(Student, form=StudentForm, max_num=1, extra=1)

