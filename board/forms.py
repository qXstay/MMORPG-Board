from django import forms
from .models import Post, Response

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'category': 'Категория',
            'title': 'Заголовок',
            'content': 'Содержание',
            'image': 'Изображение',
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите ваш отклик здесь...'
            }),
        }
        labels = {
            'text': 'Текст отклика',
        }