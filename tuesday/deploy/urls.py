from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),

    #urls for course
    path('new_course', views.new_course , name="new_course"),
    path('course', views.course , name="course"),
    path('search_course', views.search_course , name="search_course"),
    path('update_course/<str:code>',views.update_course, name="update_course"),
    path('update_course/save_update_course/<str:code>',views.save_update_course, name="save_update_course"),
    path('delete_course/<str:code>',views.delete_course, name="delete_course"),

    #urls for student
    path('new_student', views.new_student , name="new_student"),
    path('search_by_course', views.search_by_course , name="search_by_course"),

]