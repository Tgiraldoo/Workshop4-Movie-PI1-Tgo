from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movies.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Ruta del archivo JSON (ya debe estar en movie/management/commands/)
        json_file_path = os.path.join('movie', 'management', 'commands', 'movies.json')

        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f"Archivo {json_file_path} no encontrado."))
            return

        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)

        cont = 0
        for i, movie in enumerate(movies[:100]):  # solo las 100 primeras
            exist = Movie.objects.filter(title=movie['title']).first()  # evitar duplicados
            if not exist:
                try:
                    Movie.objects.create(
                        title=movie['title'],
                        image='movie/images/default.jpg',
                        genre=movie.get('genre', 'Unknown'),
                        year=movie.get('year', None),
                        description=movie.get('description', 'No description available')
                    )
                    cont += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Error cargando {movie['title']}: {e}"))
            else:
                # Si ya existe, lo actualiza
                try:
                    exist.genre = movie.get('genre', 'Unknown')
                    exist.year = movie.get('year', None)
                    exist.description = movie.get('description', 'No description available')
                    exist.image = 'movie/images/default.jpg'
                    exist.save()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Error actualizando {exist.title}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se agregaron {cont} películas a la base de datos."))
