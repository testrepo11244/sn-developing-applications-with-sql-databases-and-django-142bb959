from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Learner, Instructor


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'lesson')
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    inlines = [QuestionInline]


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Learner)
admin.site.register(Instructor)