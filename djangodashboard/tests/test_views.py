import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_dashboard_view(client):
    url = reverse("dashboard")  # Adjust name as needed
    response = client.get(url)
    assert response.status_code == 200
    assert b"Jumbotron" in response.content or b"Dashboard" in response.content