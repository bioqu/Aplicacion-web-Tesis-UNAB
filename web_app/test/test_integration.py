import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_create_order():
    client = APIClient()
    response = client.post(reverse('order-list'), {
        'product': 1,
        'quantity': 5,
        'order_date': '2024-08-25'
    })
    assert response.status_code == status.HTTP_201_CREATED
