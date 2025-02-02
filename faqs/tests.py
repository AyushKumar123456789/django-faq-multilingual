import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from faqs.models import FAQ

@pytest.mark.django_db
def test_faq_creation():
    faq = FAQ.objects.create(question="Hello World?", answer="Sample Answer")
    assert faq.id is not None
    assert faq.question == "Hello World?"

@pytest.mark.django_db
def test_faq_list_api():
    client = APIClient()
    FAQ.objects.create(question="Q1", answer="A1")
    url = reverse('faq-list-create')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['answer'] == "A1"
