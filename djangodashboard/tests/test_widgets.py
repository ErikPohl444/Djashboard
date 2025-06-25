import pytest
from dashboard.models import Widget  # Adjust import as needed

@pytest.mark.django_db
def test_widget_display_logic():
    widget = Widget.objects.create(name="Test Widget", config={"type": "alert", "color": "danger"})
    rendered = widget.render()  # Assuming you have a render method
    assert "alert-danger" in rendered
    assert "Test Widget" in rendered