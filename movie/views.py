import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from .models import Movie
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect


def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'name': 'Tomás Giraldo', 'movies': movies})




def about(request):
    return render(request, 'about.html')


def statistics_view(request):
    matplotlib.use('Agg')  

    movies = Movie.objects.all()

  
    movies_by_year = {}
    for movie in movies:
        year = movie.year if movie.year else "Unknown"
        movies_by_year[year] = movies_by_year.get(year, 0) + 1

    plt.figure(figsize=(8,5))
    plt.bar([str(k) for k in movies_by_year.keys()], movies_by_year.values())  
    plt.title("Movies per year")
    plt.xlabel("Year")
    plt.ylabel("Number of movies")
    plt.xticks(rotation=90)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    movies_by_genre = {}
    for movie in movies:
        genre = movie.genre if movie.genre else "Unknown"
        genre = genre.split(",")[0].strip()  
        movies_by_genre[genre] = movies_by_genre.get(genre, 0) + 1

    plt.figure(figsize=(8,5))
    plt.bar([str(k) for k in movies_by_genre.keys()], movies_by_genre.values())  
    plt.title("Movies per genre")
    plt.xlabel("Genre")
    plt.ylabel("Number of movies")
    plt.xticks(rotation=90)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic2 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    return render(request, 'statistics.html', {
        'graphic': graphic,
        'graphic2': graphic2
    })

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
