from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Book, Review

class BookTests(TestCase):

	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='reviewuser',
			email='reviewuser@email.com',
			password='testpass123'
		)

		self.book = Book.objects.create(
			title='The Tao Of Physics',
			author='Fritjof Kapra',
			price='22.80',
		)

		self.review = Review.objects.create(
			book=self.book,
			author=self.user,
			review='An Excellent Review',
		)

	def test_book_listing(self):
		self.assertEqual(f'{self.book.title}', 'The Tao Of Physics')
		self.assertEqual(f'{self.book.author}', 'Fritjof Kapra')
		self.assertEqual(f'{self.book.price}', '22.80')

	def test_book_list_view(self):
		response = self.client.get(reverse('book_list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'The Tao Of Physics')
		self.assertTemplateUsed(response, 'books/book_list.html')

	def test_book_detail_view(self):
		response = self.client.get(self.book.get_absolute_url())
		no_response = self.client.get('/books/`12345/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(no_response.status_code, 404)
		self.assertContains(response, 'The Tao Of Physics')
		self.assertContains(response, 'An Excellent Review')
		self.assertTemplateUsed(response, 'books/book_detail.html')

