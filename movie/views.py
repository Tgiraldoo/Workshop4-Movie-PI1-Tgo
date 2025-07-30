from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'name': 'Tomás Giraldo'})



def about(request):
    return HttpResponse("This is the About Page")
