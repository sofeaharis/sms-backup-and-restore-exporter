from django.shortcuts import render
from deploy.models import Course, Student
from django.http import  HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render (request , "index.html")

# course
def new_course(request):
    if request.method == 'POST':
        c_code = request.POST['code']
        c_desc = request.POST['desc']
        all_course = Course.objects.all()
        find =0
        for search in all_course:
            if search.code == c_code:
                find =1

        if find ==0:
            data=Course(code=c_code, desc=c_desc)
            data.save()
            msg = "Data Save"
        else:
            msg = "Course already exsis"

        dict = {
            'message': msg
        }
    else:
        dict = {
            'message':''
        }

    return render (request , "new_course.html", dict)

def course(request):
    allcourse=Course.objects.all()
    dict={
        'allcourse': allcourse
    }
    return render (request,'course.html', dict)

def search_course(request):
    if request.method == 'GET':
        data = Course.objects.filter(code = request.GET.get('c_code'))   
        dict = {
                'data': data
            }
        return render (request , "search_course.html", dict)
    else:
        return render (request , "search_course.html")
    
def update_course(request,code):
    data=Course.objects.get(code=code)
    dict = {
        'data':data
    }
    return render (request , "update_course.html", dict) 
   
def save_update_course(request,code):
    c_desc= request.POST['desc']
    data=Course.objects.get(code=code)
    data.desc = c_desc
    data.save()
    return HttpResponseRedirect(reverse("course"))

def delete_course(request,code):
    data = Course.objects.get(code=code)
    data.delete()
    return HttpResponseRedirect(reverse('course'))

# student

def new_student(request):
    allcourse=Course.objects.all()
    if request.method=='POST':
        s_id = request.POST['s_id']
        s_name = request.POST['s_name']
        s_add = request.POST['s_add']
        s_phone = request.POST['s_phone']
        s_course = request.POST['s_course']

        # get foreign key data from reference table
        s_code= Course.objects.get(code=s_course)
        data=Student(id=s_id, name=s_name, address=s_add, phone= s_phone, course_code=s_code)
        data.save()
        dict={
            'allcourse':allcourse,
            'message':"Data Save"
        }
    else:
        dict={
            'allcourse': allcourse
        }

    return render (request, 'new_student.html',dict)

def search_by_course(request):
    allcourse = Course.objects.all()
    if request.method=='GET':
        datacourse = Student.objects.filter(course_code=request.GET.get('course_code'))
        number_stud = len(datacourse)       
        dict={
            'data':datacourse,
            'allcourse': allcourse,
            'course':request.GET.get('course_code'),
            'num_stud':number_stud
        }
    else:
        dict = {
            'allcourse': allcourse
        }
    return render (request, 'search_by_course.html',dict)