from django.test import TestCase
from remanga.models import *
from django.urls import reverse

def create_title():
    Title.objects.create(manga_type = 'Западный комикс', avg_rating = 8.8 , dir_name = "the_beginning_after_the_end", 
                        rus_name = "Начало после конца", total_views = 21880713, 
                        description = "<p>Король Грей обладает непревзойденной силой, богатством и престижем в мире", 
                        img_url = "the_beginning_after_the_end/high_cover.jpg", count_bookmarks = 199119, 
                        count_chapters = 179, issue_year = 2018, total_votes = 3961645, count_rating = 28986)
    
class CatalogViewTests(TestCase): 
    def test_titles_queryset(self):    
        create_title()
        response = self.client.get("")

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context["titles_list"]), 0)

class TitleViewTests(TestCase): 
    def test_title_queryset(self):
        create_title()
        first_title_dir_name = Title.objects.all()[0].dir_name
        response = self.client.get(reverse("remanga:title", args=[first_title_dir_name])) 

        self.assertEqual(response.status_code, 200)