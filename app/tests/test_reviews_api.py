from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Review


class ReviewsAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("reviews")

        # Test user
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Create sample reviews
        self.review1 = Review.objects.create(
            user=self.user,
            title="Good song",
            artist="Artist A",
            artist_id="123",
            album="Album X",
            album_id="A1",
            content="Nice track!",
            rating=4
        )

        self.review2 = Review.objects.create(
            user=self.user,
            title="Great album",
            artist="Artist B",
            artist_id="456",
            album="Album Y",
            album_id="A2",
            content="Loved it",
            rating=5
        )

        self.review3 = Review.objects.create(
            user=self.user,
            title="Another song",
            artist="Artist A",
            artist_id="123",
            album=None,
            album_id=None,
            content="Cool!",
            rating=3
        )

    # ---------------------------
    # GET TESTS
    # ---------------------------

    def test_get_all_reviews(self):
        """Should return all reviews."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_reviews_filtered_by_artist_id(self):
        """Should return reviews for a specific artist_id."""
        response = self.client.get(self.url, {"artist_id": "123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Two reviews have artist_id="123"
        self.assertEqual(len(response.data), 2)

    def test_get_reviews_filtered_by_album_id(self):
        """Should return reviews for a specific album_id."""
        response = self.client.get(self.url, {"album_id": "A1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # One review has album_id="A1"
        self.assertEqual(len(response.data), 1)

    # ---------------------------
    # POST TESTS
    # ---------------------------

    def test_post_unauthenticated_fails(self):
        """Unauthenticated user cannot POST."""
        payload = {
            "title": "My Review",
            "artist": "Random Artist",
            "content": "Nice!",
            "rating": 5
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_authenticated_succeeds(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "title": "New Review",
            "artist": "Artist C",
            "artist_id": "789",
            "album": "Album Z",
            "album_id": "A3",
            "content": "Amazing track!",
            "rating": 5
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_data_fails(self):
        """Missing required fields should return 400."""

        client = APIClient()
        client.force_authenticate(self.user)

        payload = {
            "title": "",
            "artist": "Artist C",
            "content": "",
            "rating": ""
        }

        response = client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

