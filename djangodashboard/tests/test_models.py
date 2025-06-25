import pytest
from django.contrib.auth import get_user_model
from dashboard.models import Widget

@pytest.mark.django_db
def test_widget_creation():
    widget = Widget.objects.create(name="Test Widget", config={"type": "alert"})
    assert widget.pk is not None
    assert widget.name == "Test Widget"