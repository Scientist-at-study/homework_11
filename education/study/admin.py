from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Course, Lesson, Comment, Profile


# Register your models here.

admin.site.register(Profile)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'duration',
                    'start_date', 'price', 'get_image',)
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'start_date', 'price',)
    list_per_page = 10
    list_max_show_all = 10

    def get_image(self, obj):
        if obj.photo:
            image_url = obj.photo.url
        else:
            image_url = "https://demofree.sirv.com/nope-not-here.jpg"
        return mark_safe(f'<img src="{image_url}" width="150">')

    get_image.short_description = "Rasmi"


admin.site.register(Course, CourseAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'about',)
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title',)
    list_per_page = 10
    list_max_show_all = 10


admin.site.register(Lesson, LessonAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'user_name', 'created_at')
    list_display_links = ('id', 'lesson')
    search_fields = ('lesson__title', 'user_name')
    list_filter = ('created_at',)
    list_per_page = 10


admin.site.register(Comment, CommentAdmin)
