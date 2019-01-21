from django.urls import resolve
from lists.models import Item
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest

class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'The second list item')

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request =  HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
        ## self.assertEqual(response.content.decode(), expected_html)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>TO-DO lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        reponse = home_page(request)
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertIn("A new list item",reponse.content.decode())
