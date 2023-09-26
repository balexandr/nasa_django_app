from django.test import TestCase
from django.urls import reverse

from .views import index, get_nasa_apod, get_google_info
from unittest.mock import patch, Mock

class NasaTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch('nasa.views.get_nasa_apod')
    @patch('nasa.views.get_google_info')
    def test_index_view_context(self, mock_get_google_info, mock_get_nasa_apod):
        mock_get_nasa_apod.return_value = {"title": "Black Hole", "url": "http://space.com/blackhole.jpg", "date": "2023-09-26"}
        mock_get_google_info.return_value = {"Google Space Title": "Google Space Snippet", "Google Space Title 2": "Google Space Snippet 2"}

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        self.assertIn("url", response.context)
        self.assertIn("google_results", response.context)

    def test_get_nasa_apod(self):
        with patch('nasa.views.requests.get') as nasa_mock:
            nasa_mock.return_value.status_code = 200
            nasa_mock.return_value.json.return_value = {"title": "Black Hole", "url": "http://space.com/blackhole.jpg", "date": "2023-09-26"}
            
            nasa_data = get_nasa_apod()
            self.assertEqual(nasa_data["title"], "Black Hole")

    def test_get_google_info(self):
        with patch('nasa.views.requests.get') as google_mock:
            google_mock.return_value.status_code = 200
            google_mock.return_value.json.return_value = {
                "searchInformation": {"totalResults": "2"},
                "items": [{"title": "Google Space Title", "snippet": "Google Space Snippet"}, {"title": "Google Space Title 2", "snippet": "Google Space Snippet 2"}]
            }
            
            google_data = get_google_info("Black Hole")
            self.assertEqual(google_data["Google Space Title"], "Google Space Snippet")
