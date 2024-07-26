from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from mdeditor.fields import MDTextField


class Profile(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    
class Classify(models.Model):
    classifyname = models.CharField(max_length=100)
    available = models.BooleanField()

    def __str__(self):
        return self.classifyname

      #(Cake)
class Course(models.Model, HitCountMixin):
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    coursename = models.CharField(max_length=100)
    content = MDTextField(verbose_name='内容')
    image = models.ImageField(upload_to='course/')
    classifys = models.ManyToManyField(Classify, through="CourseClassify", through_fields=('course', 'classify'))
    price = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.IntegerField(default = 1280)
    height = models.IntegerField(default = 720)
    src = models.CharField(max_length=50, null=False)
    create_date = models.DateField(default=timezone.now)  #貼文時間
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    def __str__(self):
        return f'${self.price} - {self.coursename}'

class CourseClassify(models.Model):
    classify = models.ForeignKey(Classify, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Post(models.Model, HitCountMixin):
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)  #標題
    content = MDTextField(verbose_name='内容')  #內容
    image = models.ImageField(upload_to='course/') #(cake)
    classifys = models.ManyToManyField(Classify, through="PostClassify", through_fields=('post', 'classify'))
    create_date = models.DateField(default=timezone.now)  #貼文時間
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    def __str__(self):
        return self.__doc__ + "subject->" + self.subject
    
    class Meta:
        verbose_name = "發佈文章"
        verbose_name_plural = verbose_name

class PostClassify(models.Model):
    classify = models.ForeignKey(Classify, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     courses = models.ManyToManyField(Course, through="CartCourse")
#     # quantity = models.PositiveIntegerField(default=1)
#     def __str__(self):
#         return self.user.username

# class CartCourse(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=0)

class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    # total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default='待確認')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# class OrderCourse(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    # quantity = models.PositiveIntegerField()
