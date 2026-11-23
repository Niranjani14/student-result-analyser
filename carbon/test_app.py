import unittest
import json
from app import app
from calculator import calculate_footprint

class CarbonCalculatorTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client for Flask integrations
        self.app = app.test_client()
        self.app.testing = True

    # 1. UNIT TESTS FOR CALCULATOR LOGIC
    def test_calculator_typical_values(self):
        """Test footprint calculation under typical user input values."""
        form_data = {
            "car_type": "petrol_car",
            "car_dist": "8000",
            "public_bus": "1200",
            "public_train": "2000",
            "flights_short": "2",
            "flights_long": "2",
            "electricity": "250",
            "gas": "150",
            "diet_type": "medium_meat",
            "recycling": "partial_recycling"
        }
        res = calculate_footprint(form_data)
        self.assertIn("total", res)
        self.assertIn("categories", res)
        # Expected categories
        self.assertIn("transport", res["categories"])
        self.assertIn("energy", res["categories"])
        self.assertIn("diet", res["categories"])
        self.assertIn("waste", res["categories"])
        
        # Verify transport footprint:
        # petrol_car (8000 * 0.170) = 1360.0
        # bus (1200 * 0.080) = 96.0
        # train (2000 * 0.040) = 80.0
        # flights_short (2 * 250.0) = 500.0
        # flights_long (2 * 1500.0) = 3000.0
        # Total transport = 1360 + 96 + 80 + 500 + 3000 = 5036.0
        self.assertEqual(res["categories"]["transport"], 5036.0)

    def test_calculator_zero_values(self):
        """Test footprint calculation under boundary conditions (all zeros/none)."""
        form_data = {
            "car_type": "none",
            "car_dist": "0",
            "public_bus": "0",
            "public_train": "0",
            "flights_short": "0",
            "flights_long": "0",
            "electricity": "0",
            "gas": "0",
            "diet_type": "vegan",
            "recycling": "full_recycling"
        }
        res = calculate_footprint(form_data)
        # Expected values:
        # transport = 0.0
        # energy = 0.0
        # diet = vegan (800.0)
        # waste = full_recycling (150.0)
        # total = 950.0
        self.assertEqual(res["categories"]["transport"], 0.0)
        self.assertEqual(res["categories"]["energy"], 0.0)
        self.assertEqual(res["categories"]["diet"], 800.0)
        self.assertEqual(res["categories"]["waste"], 150.0)
        self.assertEqual(res["total"], 950.0)

    def test_calculator_negative_values_clamped(self):
        """Test that negative inputs are clamped to zero to prevent invalid negative emissions."""
        form_data = {
            "car_type": "petrol_car",
            "car_dist": "-500",
            "public_bus": "-10",
            "public_train": "-200",
            "flights_short": "-1",
            "flights_long": "-3",
            "electricity": "-250",
            "gas": "-150",
            "diet_type": "vegan",
            "recycling": "full_recycling"
        }
        res = calculate_footprint(form_data)
        self.assertEqual(res["categories"]["transport"], 0.0)
        self.assertEqual(res["categories"]["energy"], 0.0)
        self.assertEqual(res["total"], 950.0)

    # 2. INTEGRATION TESTS FOR FLASK ROUTING
    def test_get_home_page(self):
        """Test GET route to home page loads HTML structure successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EcoPulse', response.data)
        self.assertIn(b'Calculate Footprint', response.data)

    def test_post_valid_calculation(self):
        """Test POST route successfully processes dynamic inputs and returns json."""
        form_data = {
            "car_type": "hybrid_car",
            "car_dist": "5000",
            "public_bus": "100",
            "public_train": "500",
            "flights_short": "1",
            "flights_long": "0",
            "electricity": "100",
            "gas": "50",
            "diet_type": "vegetarian",
            "recycling": "full_recycling"
        }
        response = self.app.post('/', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = json.loads(response.data)
        self.assertIn("total", data)
        self.assertIn("categories", data)

    def test_post_invalid_calculation(self):
        """Test POST handles bad input types (strings instead of numbers) with 400 Bad Request."""
        form_data = {
            "car_type": "hybrid_car",
            "car_dist": "invalid_number_here",
            "public_bus": "100"
        }
        response = self.app.post('/', data=form_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    # 3. SECURITY HEADERS TESTS
    def test_security_headers_present(self):
        """Verify presence of robust security headers on response objects."""
        response = self.app.get('/')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.headers.get('X-XSS-Protection'), '1; mode=block')
        self.assertIn('Content-Security-Policy', response.headers)

if __name__ == '__main__':
    unittest.main()
