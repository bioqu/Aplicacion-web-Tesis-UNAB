from django.test import TestCase
from api.models import Product
import unittest

class ProductModelTest(unittest.TestCase):
    def setUp(self):
        Product.objects.create(name="Test Product", category="Test Category", quantity=10)

    def test_product_creation(self):
        product = Product.objects.filter(name="Test Product").first()
        self.assertIsNotNone(product, "No Product with the name 'Test Product' found.")
        self.assertEqual(product.category, "Test Category")
        self.assertEqual(product.quantity, 10)