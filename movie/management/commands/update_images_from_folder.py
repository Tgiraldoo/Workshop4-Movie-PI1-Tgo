import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from local folder (keeping original casing and spaces)"

    def handle(self, *args, **kwargs):
        images_folder = os.path.join("media", "movie", "images")

        if not os.path.exists(images_folder):
            self.stderr.write(f"Images folder not found: {images_folder}")
            return

        updated_count = 0
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in DB")

        for movie in movies:
            # Usa el título exacto, con espacios y mayúsculas
            image_filename = f"m_{movie.title}.png"
            image_path_full = os.path.join(images_folder, image_filename)

            if os.path.exists(image_path_full):
                movie.image = os.path.join("movie/images", image_filename)
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title} -> {image_filename}")

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies"))
