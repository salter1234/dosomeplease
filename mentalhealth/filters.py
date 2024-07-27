from django_filters import FilterSet, NumberFilter, CharFilter, BooleanFilter, ModelChoiceFilter
from .models import Course, Post


class CourseFilterSet(FilterSet):
    # teacher = ModelChoiceFilter(queryset=Course.objects.filter(teacher__is_teacher__exact=True).all())
    class Meta:
        model = Course
        fields = ('teacher', 'classifys')
        
        labels = {
            'teacher': '授課講師',
            'classifys': '分類',
        }

class PostFilterSet(FilterSet):
    class Meta:
        model = Post
        fields = ('teacher', 'classifys')
        
        labels = {
            'teacher': '作者',
            'classifys': '分類',
        }