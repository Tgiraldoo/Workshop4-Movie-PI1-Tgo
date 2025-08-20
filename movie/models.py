from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='movie/images/', default='movie/images/default.jpg')
    url = models.URLField(blank=True)
    genre = models.CharField(max_length=100, blank=True, null=True)  # 👈 este campo
    year = models.IntegerField(blank=True, null=True)    

    def __str__(self):
        return self.title



