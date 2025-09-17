from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Update the description of the first movie using OpenAI API"

    def handle(self, *args, **kwargs):
        # Cargar API Key desde openAI.env
        load_dotenv("openAI.env")
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        def get_completion(prompt, model="gpt-3.5-turbo"):
            messages = [{"role": "user", "content": prompt}]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0
            )
            return response.choices[0].message.content.strip()

        # Tomar solo la primera película
        movies = Movie.objects.all()
        for movie in movies:
            prompt = f"Mejora la siguiente descripción de la película '{movie.title}': {movie.description}"
            response = get_completion(prompt)
            movie.description = response
            movie.save()

            self.stdout.write(self.style.SUCCESS(f"Updated description for: {movie.title}"))
            break  
