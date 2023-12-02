from django.db import models
from django.contrib.auth.models import AbstractUser

class Genres(models.Model):
    name = models.CharField(max_length=100, default='')
   
    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return self.name

class Chapters(models.Model):
    chapter = models.IntegerField(default=0)
    tome = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-tome', '-chapter']

    def __str__(self):
        return self.chapter
        
class Title(models.Model):
    rus_name = models.CharField(max_length=100, default='')
    dir_name = models.CharField(max_length=100, default='')
    img_url = models.CharField(max_length=100, default='')
    manga_type = models.CharField(max_length=100, default='')
    avg_rating = models.FloatField(default=0.0)
    count_rating = models.IntegerField(default=0)
    issue_year = models.IntegerField(default=0)
    count_bookmarks = models.IntegerField(default=0)
    count_chapters = models.IntegerField(default=0)
    description = models.CharField(max_length=1500, default='')
    categories = models.ManyToManyField(Categories)
    genres = models.ManyToManyField(Genres)
    chapters = models.ManyToManyField(Chapters)

    def __str__(self):
        return self.rus_name

class Rating(models.Model):
    title_id = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    
class User(AbstractUser):
    titles = models.ManyToManyField(Title)
    ratings = models.ManyToManyField(Rating)
    avatar = models.ImageField(upload_to='users_avatars', null=True, blank=True)

    class Meta:
        db_table = 'auth_user'
