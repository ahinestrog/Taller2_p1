from django.shortcuts import render
from django.http import HttpResponse

from .models import Prueba

# Create your views here.
def home(request):
    #return HttpResponse('<h1>Welcome home page</h1>')
    #return render(request,'home.html')
    #return render(request,'home.html',{'name':'Alejandro Hinestroza'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Prueba.objects.filter(title__icontains=searchTerm)
    else:
        movies = Prueba.objects.all()
    return render(request,'home.html',{'searchTerm':searchTerm,'movies':movies})


def about(request):
    #return HttpResponse('<h1>About page</h1>')
    return render(request,'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request,'signup.html',{'email':email})

import matplotlib.pyplot as plt
import matplotlib
import io
import base64, urllib    

def statistics_view(request):
    matplotlib.use('Agg')

    # --- Gráfica de películas por año ---
    years = Prueba.objects.values_list('year', flat=True).distinct().order_by('year')
    
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Prueba.objects.filter(year=year)
        else:
            movies_in_year = Prueba.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras por año
    plt.figure(figsize=(10, 6))  # Crear una nueva figura para evitar sobrescribir gráficas anteriores
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    # --- Gráfica de películas por género ---
    genres = Prueba.objects.values_list('genre', flat=True)
    
    genre_counts = {}
    for genre in genres:
        first_genre = genre.split(',')[0]
        if first_genre in genre_counts:
            genre_counts[first_genre] += 1
        else:
            genre_counts[first_genre] = 1

    plt.figure(figsize=(10, 6))  # Crear una nueva figura para evitar sobrescribir gráficas anteriores
    plt.bar(genre_counts.keys(), genre_counts.values(), color='blue')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})