from django import forms
from .models import Test


class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['title', 'description', 'is_active']

from .models import Test, Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = [
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_option'
        ]