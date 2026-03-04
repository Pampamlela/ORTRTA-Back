from django.urls import reverse
from rest_framework.test import APITestCase #gère JWT, simule requêtes HTTP, teste API DRF
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Roll
from equipment.models import Camera
# Create your tests here.

User = get_user_model()

class RollAPITestCase(APITestCase):

    # création d'un utilisateurice, d'une caméra et obtention du token JWT pour les tests
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

        self.camera = Camera.objects.create(
            user=self.user,
            model="Olympus Trip 35"
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

    # test de création d'une pellicule
    def test_create_roll(self):
        data = {
            "film_name": "Kodak Portra 400",
            "film_type": "COLOR_NEGATIVE",
            "camera": self.camera.id,
            "iso": 400,
            "format": "35MM-12",
            "date_start": "2026-01-01",
        }

        response = self.client.post("/api/rolls/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Roll.objects.count(), 1)
        self.assertEqual(Roll.objects.first().user, self.user)

    # test d'accès à une pellicule sans authentification
    def test_authentication_required(self):
        self.client.credentials() #enlève le token

        response = self.client.get("/api/rolls/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test d'accès à une pellicule d'un autre utilisateur
    def test_cannot_access_othe_user_roll(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="otherpassword"
        )

        roll = Roll.objects.create(
            user=other_user,
            camera=self.camera,
            film_name="Kodak Tri-X 400",
            film_type="BLACK_AND_WHITE",
            iso=400,
            format="35MM-24",
            date_start="2026-01-01",
        )

        response = self.client.get(f"/api/rolls/{roll.slug}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test roll scanné ne peut plus être modifié
    def test_scanned_roll_cannot_be_modified(self):
        roll = Roll.objects.create(
            user=self.user,
            camera=self.camera,
            film_name="Porta 400",
            film_type="COLOR_NEGATIVE",
            iso=400,
            format="35MM-12",
            date_start="2026-01-01",
            date_scan="2026-01-10"
        )

        response = self.client.patch(
            f"/api/rolls/{roll.slug}/", 
            {"iso": 800}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test du changement de statut vers "SCANNED" lors de la définition de date_scan
    def test_status_becomes_scanned_when_date_scan_set(self):
        roll = Roll.objects.create(
            user=self.user,
            camera=self.camera,
            film_name="Porta 400",
            film_type="COLOR_NEGATIVE",
            iso=400,
            format="35MM-36",
            date_start="2026-01-01",
            date_scan="2026-01-10"
        )

        roll.refresh_from_db() # force Django à relire la base de données pour obtenir les dernières valeurs

        self.assertEqual(roll.status, "SCANNED")

    # test de l'endpoint de génération de QR code
    def test_qr_endpoint_returns_png(self):
        roll = Roll.objects.create(
            user=self.user,
            camera=self.camera,
            film_name="Kodak Gold 200",
            film_type="COLOR_NEGATIVE",
            iso=200,
            format="35MM-36",
            date_start="2026-01-01",
        )

        response = self.client.get(f"/api/rolls/{roll.slug}/qr/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertTrue(len(response.content) > 0)
        self.assertTrue(response.content.startswith(b"\x89PNG"))