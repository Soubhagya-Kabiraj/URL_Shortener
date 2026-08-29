# UPDATED CODE: SnapURL Dashboard Logic
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import shortURL

class SnapURLTestCase(TestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Create short URLs for user1
        self.url1 = shortURL.objects.create(user=self.user1, original_url='https://google.com', short_code='goog1')
        self.url2 = shortURL.objects.create(user=self.user1, original_url='https://github.com', short_code='git1')

        # Create short URL for user2
        self.url3 = shortURL.objects.create(user=self.user2, original_url='https://stackoverflow.com', short_code='so1')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')

    def test_dashboard_metrics_and_isolation(self):
        # Log in as user1
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Verify counts in context
        self.assertEqual(response.context['total_urls'], 2)
        self.assertEqual(response.context['total_history'], 2)
        
        # Verify user2's url is not in recent activities for user1
        activities = response.context['recent_activities']
        self.assertEqual(len(activities), 2)
        self.assertNotIn(self.url3, activities)

    def test_search_history_isolation(self):
        # Log in as user1
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        
        urls = response.context['urls']
        self.assertEqual(urls.count(), 2)
        self.assertNotIn(self.url3, urls)

    def test_shorten_url_associates_with_user(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('shorten_url'), {'original_url': 'https://python.org'})
        self.assertRedirects(response, reverse('home'))
        
        # Check that the new url is associated with user1
        new_url = shortURL.objects.filter(user=self.user1, original_url='https://python.org').first()
        self.assertIsNotNone(new_url)
        self.assertEqual(new_url.user, self.user1)

    def test_cannot_delete_other_user_url(self):
        # Log in as user1
        self.client.login(username='user1', password='password123')
        
        # Try to delete user2's url
        response = self.client.post(reverse('delete_url', args=[self.url3.id]))
        # Should return 404 since get_object_or_404 filters by user=request.user
        self.assertEqual(response.status_code, 404)
        
        # Verify url3 still exists
        self.assertTrue(shortURL.objects.filter(id=self.url3.id).exists())

    def test_can_delete_own_url(self):
        # Log in as user1
        self.client.login(username='user1', password='password123')
        
        # Delete own url
        response = self.client.post(reverse('delete_url', args=[self.url1.id]))
        self.assertRedirects(response, reverse('home'))
        
        # Verify url1 is deleted
        self.assertFalse(shortURL.objects.filter(id=self.url1.id).exists())
