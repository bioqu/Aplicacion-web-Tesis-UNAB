from django.test import TestCase
from .models import Product
import unittest

class ProductModelTest(unittest.TestCase):
    def setUp(self):
        Product.objects.filter(name="Test Product").delete()  # Elimina los productos con el nombre dado
        Product.objects.create(name="Test Product", category="Test Category", quantity=10)

    def test_product_creation(self):
        products = Product.objects.filter(name="Test Product")
        self.assertEqual(products.count(), 1, "Expected exactly one product, found: {}".format(products.count()))
        product = products.first()
        self.assertEqual(product.category, "Test Category")
        self.assertEqual(product.quantity, 10)