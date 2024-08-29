from django.test import TestCase

# Create your tests here.
from api.models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        Product.objects.create(name="Test Product", category="Test Category", quantity=10)

    def test_product_creation(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.category, "Test Category")
        self.assertEqual(product.quantity, 10)