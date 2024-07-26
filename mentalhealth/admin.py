from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Classify, Course, CourseClassify, Order, Post, PostClassify
from .forms import ProfileForm

class CustomUserAdmin(UserAdmin):
    add_form = ProfileForm
    model = Profile
    list_display = ('username', 'email', 'is_student', 'is_teacher', 'is_approved', 'is_staff')
    list_filter = ('is_student', 'is_teacher', 'is_approved',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Personal info', {'fields': ('address', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_approved', 'is_student', 'is_teacher')})
    )
    add_fieldsets = (
        ("Required Information", {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_student', 'is_teacher', 'is_approved')
        }),
        ("Optional Information", {
            'classes': ('wide',),
            'fields': ('address', 'phone')
        }),
    )
    search_fields = ('email',)
    ordering = ('username',)

admin.site.register(Profile, CustomUserAdmin)

class ClassifyAdmin(admin.ModelAdmin):
    list_display = ('classifyname', 'available')
    list_filter = ('available',)
    fieldsets = (
        (None, {'fields': ('classifyname',)}),
        ('Permissions', {'fields': ('available',)})
    )
    search_fields = ('classify__classifyname',)
admin.site.register(Classify, ClassifyAdmin)


#===================================================
class CourseClassifyInline(admin.TabularInline):
    model = CourseClassify
class CourseAdmin(admin.ModelAdmin): 
    list_display = ('id', 'teacher', 'coursename', 'create_date', 'price', 'formatted_hit_count')
    def formatted_hit_count(self, course: Course):
        return course.hit_count.hits if hasattr(course, 'hit_count') else 'N/A'
    formatted_hit_count.admin_order_field = 'hit_count'
    formatted_hit_count.short_description = 'Hits'
    list_filter = ('teacher', 'classifys', 'hit_count_generic',) 
    fieldsets = (
        (None, {'fields': ('teacher',)}),
        ('Courses info', {'fields': ('coursename', 'content', 'price', 'create_date')}),
        ('Srcs', {'fields': ('src',)}),
        ('Image', {'fields': ('image',)}),
    )
    search_fields = ('coursename',)
    ordering = ('-create_date',)
    inlines = [CourseClassifyInline]
admin.site.register(Course, CourseAdmin)

class CourseClassifyAdmin(admin.ModelAdmin):
    list_display = ('course','classify')
    list_filter = ('classify',)
    search_fields = ('course',)
admin.site.register(CourseClassify, CourseClassifyAdmin)
#===================================================
class PostClassifyInline(admin.TabularInline):
    model = PostClassify

class PostAdmin(admin.ModelAdmin):
    inlines = [PostClassifyInline]
    list_display = ['teacher', 'subject', 'create_date','formatted_hit_count']
    def formatted_hit_count(self, post: Post):
        return post.hit_count.hits if hasattr(post, 'hit_count') else 'N/A'
    formatted_hit_count.admin_order_field = 'hit_count'
    formatted_hit_count.short_description = 'Hits'
    list_filter = ('teacher', 'classifys', 'hit_count_generic',)
    fieldsets = (
        (None, {'fields': ('teacher',)}),
        ('Posts info', {'fields': ('subject', 'content', 'create_date')}),
        ('Image', {'fields': ('image',)}),
    )
    search_fields = ('subject',)
    ordering = ('-create_date',)
admin.site.register(Post, PostAdmin)

class PostClassifyAdmin(admin.ModelAdmin):
    list_display = ('post','classify')
    list_filter = ('classify',)
    search_fields = ('post',)
admin.site.register(PostClassify, PostClassifyAdmin)
#===================================================
# class OrderCourseInline(admin.TabularInline):
#     model=OrderCourse
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # inlines = [OrderCourseInline]
    list_display = ['courses', 'user', 'status', 'created_time']
    list_filter = ('status', 'created_time',)
    autocomplete_fields = ['courses']
    ordering = ('-created_time',)
# admin.site.register(Order, OrderAdmin)

