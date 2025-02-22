from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="user/profile", null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kurs nomi")
    description = models.TextField(verbose_name="kurs tavfsifi")
    photo = models.ImageField(upload_to="course/photos", null=True, blank=True, verbose_name="Rasmi")
    duration = models.CharField(max_length=100, verbose_name="Kurs davomiyligi")
    start_date = models.DateField(verbose_name="Kursni boshlanish sanasi")
    price = models.IntegerField(verbose_name="Kursning narhi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Kurslar"
        verbose_name = "Kurs"


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Darsning nomi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE,  verbose_name="Kurs")
    about = models.TextField(verbose_name="Dars haqida qisqacha malumot", null=True, blank=True)

    def __str__(self):
        return f"{self.course.name} - {self.title}"

    class Meta:
        verbose_name_plural = "Darslar"
        verbose_name = "Dars"


class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Darsning nomi")
    user_name = models.CharField(max_length=100, verbose_name="Foydalanuvchi ismi")
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Izoh qilingan vaqt")

    def __str__(self):
        return f"{self.user_name} - {self.lesson}"

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ["-created_at"]