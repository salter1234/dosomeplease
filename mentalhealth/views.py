from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .models import Course, Order, Post, CourseClassify,Classify
from .forms import ProfileForm, CourseForm, PostForm, OrderForm
import logging
from .filters import CourseFilterSet, PostFilterSet
import markdown


logger = logging.getLogger(__name__)

#student首頁商品呈現
def index(request):
    courselis=[]
    courses = Course.objects.filter().order_by('-create_date')[:6]
    for course in courses:
        course.content = markdown.markdown(course.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],
                                  safe_mode=True,
                                  enable_attributes=False)
        courselis.append(course)

    postlis=[]
    posts = Post.objects.filter().order_by('-create_date')[:6]
    for post in posts:
        post.content = markdown.markdown(post.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],
                                  safe_mode=True,
                                  enable_attributes=False)
        postlis.append(post)
    return render(request, 'mentalhealth/index.html', {'courselis': courselis,
                                                       'postlis': postlis})

#teacher首頁商品呈現
def index_teacher(request):
    courselis=[]
    courses = Course.objects.filter().order_by('-create_date')[:6]
    for course in courses:
        course.content = markdown.markdown(course.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],
                                  safe_mode=True,
                                  enable_attributes=False)
        courselis.append(course)

    postlis=[]
    posts = Post.objects.filter().order_by('-create_date')[:6]
    for post in posts:
        post.content = markdown.markdown(post.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],
                                  safe_mode=True,
                                  enable_attributes=False)
        postlis.append(post)
    return render(request, 'mentalhealth/index.html', {'courselis': courselis,
                                                       'postlis': postlis})

#用戶註冊
def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.is_active = False  #用戶註冊後需要管理員審核
            profile.save()
            return redirect('login')
    else:
        # form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'mentalhealth/register.html', {'profile_form': profile_form})#'form': form, 

#登入
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_approved:
                login(request, user)
                if user.is_student:
                    return redirect('index')
                elif user.is_teacher:
                    return redirect('index_teacher')
            else:
                return render(request, 'mentalhealth/login.html', {"form": form, "error": "用戶註冊後需要管理員審核，請耐心等候！"})
            
    else:
        form = AuthenticationForm()
    return render(request, 'mentalhealth/login.html', {'form': form})

#登出
@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


#order
@login_required(login_url= '/login/') #會檢測使用者是否已經登入，若已登入才會執行add_to_cart()的程式
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) #commit=False讓表單所得數據先不儲存到資料庫，先指派order標籤
            order.user = request.user #新增model有，但是forms沒有讓輸入的數據
            order.save() #再全部一起儲存到資料庫
            # form.save_m2m() #儲存多對多關聯數據。如果你直接使用save()或form_valid()方法，是可以直接存储多对多(m2m)关系的，但是上面我們用了commit=False，所以需要如此。
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'mentalhealth/order.html', {'form': form})


@login_required
def order_confirmation(request, order_id):
    try:
        orders = Order.objects.filter(user=request.user, status='待確認')
        total_price = sum(order.courses.price for order in orders)
        if request.method == 'POST':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                new_order = order_form.save(commit=False)
                new_order.user = request.user
                # new_order.status = 'Pending'
                new_order.save()
                # order_form.save_m2m()
                return redirect('order_confirmation', order_id=new_order.id)
    except ObjectDoesNotExist:
        logger.error("訂單不存在")
        return redirect('index')

    order_totals = []
    for order in orders:
        order_total = order.courses.price
        order_totals.append({
            'order': order,
            'order_total': order_total
        })

    return render(request, 'mentalhealth/order_confirmation.html', {
        'orders': order_totals,
        'order_price': total_price,
        'order_form':OrderForm(),
        'order_id': order_id
        })


@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='待確認')
    order.delete()
    return redirect('order_confirmation', order_id=order_id)

@login_required
def add_item_to_order(request, order_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.save()
    return redirect('order_confirmation', order_id=order_id)

@login_required
def order_confirm(request, order_id):
    try:
        orders = Order.objects.filter(user=request.user, status='待確認')
        total_price = sum(order.courses.price for order in orders)
        try:
            # Send confirmation email
            send_mail(
                'DoSome心理健康學習平台 訂閱確認',
                f'非常感謝您的訂閱, {request.user.username}。 您訂閱的課程如下：\n\n' + '\n'.join([f'課程名稱：{order.courses.coursename}' for order in orders]) + f'\n\n總金額： ${total_price:.2f}.',
                'your-email@gmail.com',  # Replace with your actual email address
                [request.user.email],
                fail_silently=False,
            )
            orders.update(status='已訂閱')
            return redirect('order_history')
        except Exception as e:
            logger.error(f"Error sending email: {e}")
    except ObjectDoesNotExist:
        logger.error("訂單不存在")
    return redirect('index')

#order_history
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'mentalhealth/order_history.html', {'orders': orders})

#course
def course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.content = markdown.markdown(course.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],
                                  safe_mode=True,
                                  enable_attributes=False)
    return render(request, 'mentalhealth/course.html', {'course': course})

#courses
def courses(request):
    courses = Course.objects.filter().all().order_by('-create_date')
    filter_class = CourseFilterSet(request.GET, queryset=courses)
    for course in filter_class.qs:
        course.content = markdown.markdown(course.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],
                                  safe_mode=True,
                                  enable_attributes=False)
    return render(request, 'mentalhealth/courses.html', {'filter':filter_class})

#post
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.content = markdown.markdown(post.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],
                                  safe_mode=True,
                                  enable_attributes=False)
    return render(request, 'mentalhealth/post.html', {'post': post})

#posts
def posts(request):
    posts = Post.objects.filter().all().order_by('-create_date')
    filter_class = PostFilterSet(request.GET, queryset=posts)
    for post in filter_class.qs:
        post.content = markdown.markdown(post.content,
                                     extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ],
                                  safe_mode=True,
                                  enable_attributes=False)
    
    return render(request, 'mentalhealth/posts.html', {'filter':filter_class})

#writePosts
@login_required
def writePosts(request):
    posts = Post.objects.filter(teacher_id=request.user).order_by("create_date").all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) #commit=False讓表單所得數據先不儲存到資料庫
            post.teacher = request.user #新增model有，但是forms沒有讓輸入的數據
            post.create_date = form.cleaned_data['create_date']
            post.save() #再全部一起儲存到資料庫
            form.save_m2m()
            # print(post.image.url)
            return redirect('writePosts')
    else:
        form = PostForm()
    return render(request, 'mentalhealth/writePosts.html', 
                  {'posts': posts, 'form': form}
                  )

#writePostsCreate
@login_required
def writePostsDelete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('writePosts')

#writePostsUpdate
@login_required
def writePostsUpdate(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.save()
            return redirect('post', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'mentalhealth/writePostsUpdate.html',{'post': post, 'form': form})

# writeCourses
@login_required
def writeCourses(request):
    courses = Course.objects.filter(teacher_id=request.user).order_by("create_date").all()
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False) #commit=False讓表單所得數據先不儲存到資料庫
            course.teacher = request.user #新增model有，但是forms沒有讓輸入的數據
            course.create_date = form.cleaned_data['create_date']
            course.save() #再全部一起儲存到資料庫
            form.save_m2m()
            # print(post.image.url)
            return redirect('writeCourses')
    else:
        form = CourseForm()
    return render(request, 'mentalhealth/writeCourses.html', 
                  {'courses': courses, 'form': form}
                  )

#writeCoursesCreate
@login_required
def writeCoursesDelete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('writeCourses')

#writeCoursesUpdate
@login_required
def writeCoursesUpdate(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course.save()
            return redirect('course', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'mentalhealth/writeCoursesUpdate.html',
                  {'course': course, 'form': form}
                  )