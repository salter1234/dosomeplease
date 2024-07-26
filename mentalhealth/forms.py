from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Profile, Order, Course, Classify, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django.utils import timezone

class ProfileForm(UserCreationForm):   
    class Meta:
        model = Profile
        fields = ['username', 'password1', 'password2', 'email', 'address', 'phone', 'is_student', 'is_teacher']
        labels = {
            'username': '用戶名',
            'password1': '密碼',
            'password2': '輸入相同密碼',
            'email': '電子郵件',
            'address': '通訊地址',
            'phone': '聯絡電話',
            'is_student': '我是訂閱者',
            'is_teacher': '我是作者'
        }

class CourseForm(forms.ModelForm):
    classifys = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                               queryset=Classify.objects.all(), 
                                               label = '分類')
    class Meta:
        model = Course
        fields = ('coursename', 'content', 'classifys', 'price', 'image', 'src')
        
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['coursename'].label = '課程名稱'
        self.fields['content'].label = '課程簡介'
        self.fields['price'].label = '價格'
        self.fields['image'].label = '上傳圖片'
        self.fields['src'].label = '影片嵌入位址'
        
class OrderForm(forms.ModelForm):
    courses = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="選擇課程", 
                                               label = '課程名稱')
    class Meta:
        model = Order
        fields = ['courses']
        labels = {
            'courses': '課程'
        }


class PostForm(forms.ModelForm):
    subject = forms.CharField(max_length=255, label = '文章標題', required=True)
    classifys = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple, 
                                               queryset=Classify.objects.all(), 
                                               label = '分類')
    class Meta:
        model = Post
        fields = ('subject', 'content', 'classifys', 'image')
        labels = {
            'subject': '文章標題',
            'content': '文章內容',
            'image': '上傳圖片'
        }