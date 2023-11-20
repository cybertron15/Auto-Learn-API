from .models import CourseInfo
from django import forms
class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = ['course', 'level_info', 'courseid']