from django import forms

from mailing.models import Mailing


class MailingCreateForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['name', 'subject', 'message', 'to_users','attachment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Poçt adı'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Mesajın başlığı'}),
            'message': forms.Textarea(attrs={'placeholder': 'Mesaj mətni'}),
        }
