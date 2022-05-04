from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.views import APIView

from cinema.serializers import GenreSerializer
from cinema.models import Genre
from cinema.views import GenreList, GenreDetail


class GenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Genre.objects.create(
            id=1,
            name="Comedy",
        )
        Genre.objects.create(
            id=2,
            name="Drama",
        )

    def test_genre_list_is_subclass(self):
        self.assertEqual(issubclass(GenreList, APIView), True)

    def test_genre_detail_is_subclass(self):
        self.assertEqual(issubclass(GenreDetail, APIView), True)

    def test_get_genres(self):
        response = self.client.get("/api/cinema/genres/")
        serializer = GenreSerializer(Genre.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_genres(self):
        response = self.client.post(
            "/api/cinema/genres/",
            {
                "id": 3,
                "name": "Sci-fi",
            },
        )
        db_genres = Genre.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_genres.count(), 3)
        self.assertEqual(db_genres.get(id=3).name, "Sci-fi")

    def test_get_genre(self):
        response = self.client.get("/api/cinema/genres/2/")
        serializer = GenreSerializer(
            Genre(
                id=2,
                name="Drama",
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_genre(self):
        response = self.client.get("/api/cinema/genres/1001/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_genre(self):
        response = self.client.put(
            "/api/cinema/genres/1/",
            {
                "name": "Sci-fi",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_genre(self):
        response = self.client.patch(
            "/api/cinema/genres/1/",
            {
                "name": "Sci-fi",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_genre(self):
        response = self.client.delete(
            "/api/cinema/genres/1/",
        )
        db_genres_id_1 = Genre.objects.filter(id=1)
        self.assertEqual(db_genres_id_1.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_genre(self):
        response = self.client.delete(
            "/api/cinema/genres/1000/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)