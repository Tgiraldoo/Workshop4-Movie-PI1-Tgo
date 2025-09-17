import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Check stored embeddings"

    def handle(self, *args, **kwargs):
        for movie in Movie.objects.all()[:5]:  # solo las primeras 5
            emb_array = np.frombuffer(movie.emb, dtype=np.float32)
            self.stdout.write(f"{movie.title} -> First values: {emb_array[:5]}")
