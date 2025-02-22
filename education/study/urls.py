from django.urls import path
from .views import (index, course_detail, lesson_detail,
                    delete_comment, user_login, user_register, user_logout, profile)


urlpatterns = [
    path('', index, name='home'),
    path('course/<int:course_id>', course_detail, name="course_detail"),
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),

]
