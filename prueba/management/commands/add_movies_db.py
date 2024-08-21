from django.core.management.base import BaseCommand
from prueba.models import Prueba
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        # Recuerde que la consola está ubicada en la carpeta DjangoProjectBase.
        # El path del archivo movie_descriptions con respecto a DjangoProjectBase sería la carpeta anterior
        json_file_path = 'prueba/management/commands/movies.json'

        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            movies = json.load(file)

        # Add products to the database
        for i in range(100):
            movie = movies[i]
            exist = Prueba.objects.filter(title=movie['title']).first() # Se asegura que la película no exista en la base de datos
            if not exist:
                Prueba.objects.create(title=movie['title'],
                                     image = 'media/prueba/images/default.jpg',
                                     genre = movie['genre'],
                                     year = movie['year'])

        # self.stdout.write(self.style.SUCCESS(f'Successfully added {count} products to the database'))
