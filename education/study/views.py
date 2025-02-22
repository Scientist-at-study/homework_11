from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from .models import Course, Lesson, Comment, Profile
from .forms import CommentForm, LoginForm, RegisterForm


def index(request: HttpRequest):
    courses = Course.objects.all()
    lessons = Lesson.objects.all()
    context = {
        "courses": courses,
        "lessons": lessons
    }
    return render(request, "index.html", context)


def course_detail(request: HttpRequest, course_id):
    course = Course.objects.get(pk=course_id)
    lessons = Lesson.objects.filter(course=course)
    context = {
        "course": course,
        "lessons": lessons
    }
    return render(request, "course_detail.html", context)


@login_required
# @permission_required('study.view_lesson', raise_exception=True)
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    comments = Comment.objects.filter(lesson=lesson).order_by("-created_at")

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Izoh qoldirish uchun royhatdan oting!")
            return redirect("login")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Создаем комментарий, но не сохраняем
            comment.lesson = lesson  # Привязываем комментарий к уроку
            comment.user_name = request.user.username  # Устанавливаем имя пользователя
            comment.save()  # Сохраняем в базу
            messages.success(request, "Izohingiz qoshildi ☜(ﾟヮﾟ☜)")
            return redirect("lesson_detail", lesson_id=lesson.id)
        else:
            messages.error(request, "Hatolik yuz berdi 🤔🤔🤔")
    else:
        form = CommentForm()

    return render(request, "lesson_detail.html", {"lesson": lesson, "comments": comments, "form": form})


@permission_required("study.delete_comment", raise_exception=True)
def delete_comment(request: HttpRequest, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if not request.user.is_authenticated:
        messages.error(request, "Izohni o‘chirish uchun avval tizimga kiring!")
        return redirect("login")

    if comment.user_name != request.user.username:
        messages.error(request, "Siz faqat o‘z izohlaringizni o‘chirishingiz mumkin!")
        return redirect("lesson_detail", lesson_id=comment.lesson.id)

    lesson_id = comment.lesson.id
    comment.delete()
    messages.success(request, "Izoh o‘chirildi!")
    return redirect("lesson_detail", lesson_id=lesson_id)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz {user.username} ☜(ﾟヮﾟ☜)")
            return redirect('home')
    else:
        form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "auth/login.html", context)


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Akkaunt muvaffaqiyatli qo'shildi!\n"
                                      "Iltimos login parolni terib kiring!")
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        "form": form
    }
    return render(request, 'auth/register.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, "Siz akkauntdan chiqdingiz ☹!")
    return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        context = {}
        try:
            profile = Profile.objects.get(user=request.user)
            context['profile'] = profile
        except:
            pass
        return render(request, "auth/profile.html", context)
    else:
        messages.warning(request, "Siz kimsiz (T_T)")
        return redirect('home')

# ----------------------------------User login old version-----------------------------

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         messages.success(request, f"Xush kelibsiz {user.username} ☜(ﾟヮﾟ☜)")
#         return redirect('home')
#
#     return render(request, "auth/login.html")

# --------------------------------------Register---------------------------------------
# def user_register(request):
#     if request.method == 'POST':
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")
#         if password1 == password2:
#             user = User.objects.create_user(username=username, email=email, password=password1)
#             messages.success(request, "Akkaunt muvaffaqiyatli qo'shildi!\n"
#                                       "Iltimos login parolni terib kiring!")
#             return redirect('login')
#     return render(request, 'auth/register.html')
