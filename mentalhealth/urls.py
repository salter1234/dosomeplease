from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("teacher/", views.index_teacher, name='index_teacher'),
    path("register/", views.register, name='register'),
    path("logout/", views.user_logout, name='logout'),
    path("login/", views.user_login, name='login'),
    path("order/", views.order, name='order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path("order_history/", views.order_history, name='order_history'),
    path("order_delete/<int:order_id>/", views.order_delete, name='order_delete'),
    path("order_confirm/<int:order_id>/", views.order_confirm, name='order_confirm'),
    path("add_item_to_order/<int:order_id>/", views.add_item_to_order, name='add_item_to_order'),
    path("course/<int:course_id>/", views.course, name='course'),
    path("courses/", views.courses, name='courses'),
    path("post/<int:post_id>/", views.post, name='post'),
    path("posts/", views.posts, name='posts'),
    path("writePosts/", views.writePosts, name='writePosts'),
    path("writePosts/update/<int:post_id>/", views.writePostsUpdate, name='writePostsUpdate'),
    path("writePosts/delete/<int:post_id>/", views.writePostsDelete, name='writePostsDelete'),
    path("writeCourses/", views.writeCourses, name='writeCourses'),
    path("writeCourses/<int:course_id>/update/", views.writeCoursesUpdate, name='writeCoursesUpdate'),
    path("writeCourses/<int:course_id>/delete/", views.writeCoursesDelete, name='writeCoursesDelete'),
]