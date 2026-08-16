from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('courses/<int:course_id>/submit/', views.submit, name='submit'),
    path('courses/<int:course_id>/result/<int:submission_id>/',
         views.show_exam_result,
         name='show_exam_result'),
]