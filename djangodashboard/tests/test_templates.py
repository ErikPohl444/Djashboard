import pytest
from django.template.loader import render_to_string

def test_dashboard_template_renders():
    html = render_to_string("dashboard/dashboard.html", {"widgets": []})
    assert "Dashboard" in html
    # Add more checks for expected template content