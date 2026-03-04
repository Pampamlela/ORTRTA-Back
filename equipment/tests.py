from django.urls import reverse
from rest_framework.test import APITestCase #gère JWT, simule requêtes HTTP, teste API DRF
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Camera, Lens

# Create your tests here.

User = get_user_model()

class EquipmentAPITestCase(APITestCase):

    # création de deux utilisateurices et obtention du token JWT pour les tests
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="otherpassword"
        )

        #Login JWT
        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": "testuser", 
                "password": "testpassword"
            },
        )

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    # test création appareil photo
    def test_create_camera(self):
        data = {
            "model": "Olympus Trip 35",
        }

        response = self.client.post("/api/cameras/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Camera.objects.count(), 1)
        self.assertEqual(Camera.objects.first().user, self.user)

    # test accès à l'appareil photo d'un autre utilisateur
    def test_cannot_acces_other_user_camera(self):
        camera = Camera.objects.create(
            user=self.other_user,
            model="Nikon F3"
        )

        response = self.client.get(f"/api/cameras/{camera.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test tentative d'attachement d'un appareil photo d'un autre utilisateur à un objectif
    def test_cannot_atach_other_user_camera_to_lens(self):
        other_camera = Camera.objects.create(
            user=self.other_user,
            model="Nikon F3"
        )

        data = {
            "model": "50mm f/1.8",
            "cameras": [other_camera.id]
        }

        response = self.client.post("/api/lenses/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

