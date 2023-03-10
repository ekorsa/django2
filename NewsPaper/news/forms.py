from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'post_type',
            'author',
            'post_category',
        ]

    def clean_name(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return title
