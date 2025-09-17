import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Calculate cosine similarity between movies or between a prompt and movies"

    def handle(self, *args, **kwargs):
      
        load_dotenv("openAI.env")
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        
        try:
            movie1 = Movie.objects.get(title="Carmencita")
            movie2 = Movie.objects.get(title="Blacksmith Scene")
        except Movie.DoesNotExist as e:
            self.stderr.write(f"Error: {e}")
            return

        
        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"🎬 {movie1.title} vs {movie2.title}: {similarity:.4f}")

        
        prompt = "old short black and white film"  
        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"📝 Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"📝 Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")
