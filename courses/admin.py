from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path

from .models import Category, Course, Lesson, Tag



class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()
# zzzz
    def stats_view(self, request):
        count = Course.objects.filter(active=True).count()
        stats = Course.objects.annotate(lesson_count=Count('my_lesson')).values('id', 'subject', 'lesson_count')
        print(stats)

        labels = []
        data = []

        for course in stats:
            labels.append(course['subject'])
            data.append(course['lesson_count'])


        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': count,
            'course_stats': stats,
            'labels': labels,
            'data': data
        })

admin_site = CourseAppAdminSite(name='myadmin')

class LessonTagInlineAdmin(admin.TabularInline):
    model = Lesson.tags.through

class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'get_name']
    inlines = [LessonTagInlineAdmin, ]

    def get_name(self, obj):
        return obj.course.subject

    get_name.short_description = 'Course'  # Renames column head

class TagAdmin(admin.ModelAdmin):
    inlines = [LessonTagInlineAdmin, ]

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description']


# Register your models here.
admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag, TagAdmin)
