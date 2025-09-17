import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Generate and store embeddings for all movies"

    def handle(self, *args, **kwargs):
      
        load_dotenv("openAI.env")
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        for movie in movies:
            try:
                response = client.embeddings.create(
                    input=[movie.description],
                    model="text-embedding-3-small"
                )
                emb_array = np.array(response.data[0].embedding, dtype=np.float32)
                movie.emb = emb_array.tobytes()
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"👌 Embedding stored for: {movie.title}"))
            except Exception as e:
                self.stderr.write(f"❌ Error with {movie.title}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("🌟 Finished generating embeddings for all movies"))
