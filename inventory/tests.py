from functools import partial
from rest_framework import status
from django.urls import reverse
from .models import Book
from authentication.tests.test_login import SetLogin

name = 'My Life'
description = 'Just another sample'


class BooksTest(SetLogin):
    base_url = reverse('inventory:book-list')
    url_with_args = partial(reverse, 'inventory:book-detail')

    def setUp(self):
        # Login Given User
        self.token = super(BooksTest, self).setUp()

        # Create given book
        self.book = Book.objects.create(name=name, description=description)

    def test_list_books(self):
        """
        Get set of books
        """
        # Client sends a get request
        response = self.client.get(
            self.base_url, HTTP_AUTHORIZATION=f'JWT {self.token}')

        # Status Code returned by the API must be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # API must return the correct data
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], name)
        self.assertEqual(response.data[0]['description'], description)

    def test_create_book(self):
        # Client sends the book that he wants to add
        data = {'name': 'Just another life', 'description': 'Another Sample'}
        response = self.client.post(self.base_url,
                                    data,
                                    HTTP_AUTHORIZATION=f'JWT {self.token}')

        # Status Code returned by the API must be 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # API must return created book
        self.assertEqual(Book.objects.filter(name=self.book.name).count(), 1)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])

    def test_get_book(self):
        # Client sends the book that he wants to check
        response = self.client.get(self.url_with_args(
            kwargs={'pk': self.book.id}),
            HTTP_AUTHORIZATION=f'JWT {self.token}')

        # Status Code returned by the API must be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # API must return the book requested
        self.assertEqual(response.data['name'], self.book.name)
        self.assertEqual(response.data['description'], self.book.description)

    def test_update_book(self):
        # Client sends the book that he wants to update with the updated data
        data = {'name': f'{self.book.name} 2',
                'description': f'{self.book.description} 2'}
        response = self.client.put(self.url_with_args(
            kwargs={'pk': self.book.id}),
            data,
            HTTP_AUTHORIZATION=f'JWT {self.token}')

        # Status Code returned by the API must be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # API must return the book requested
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])

    def test_delete_book(self):
        # Client sends the book that he wants to delete
        response = self.client.delete(self.url_with_args(
            kwargs={'pk': self.book.id}),
            HTTP_AUTHORIZATION=f'JWT {self.token}')

        # Status Code returned by the API must be 200
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if book still exist
        self.assertEqual(Book.objects.filter(name=self.book.name).count(), 0)
