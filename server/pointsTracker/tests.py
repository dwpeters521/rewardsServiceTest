import django
import json
import pytest
import pytz

from datetime import datetime, timedelta
from django.test import TestCase, Client

from pointsTracker.models import PayerBalance, Transaction


class PointsTrackerTestCase(TestCase):

    def setUp(self):
        django.setup()

        super(PointsTrackerTestCase, self).setUp()

        self.web_client = Client()

    @pytest.mark.django_db
    def test_add_transaction_success(self):
        datetime_obj = datetime(year=2021, month=3, day=31, hour=10, minute=20, second=30)
        datetime_obj = pytz.utc.localize(datetime_obj)
        datetime_str = datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')

        request_data_1 = {
            'payer': 'Rusty Shackleford',
            'points': 1000,
            'timestamp': datetime_str
        }

        response_1 = self.web_client.post('/add-transaction/', request_data_1, content_type='application/json')
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(
            1,
            Transaction.objects.filter(
                payer='Rusty Shackleford', points=1000, timestamp=datetime_obj
            ).count()
        )

        request_data_2 = {
            'payer': 'Rusty Shackleford',
            'points': -1000,
            'timestamp': datetime_str
        }

        response_2 = self.web_client.post('/add-transaction/', request_data_2, content_type='application/json')
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(
            1,
            Transaction.objects.filter(
                payer='Rusty Shackleford', points=0, timestamp=datetime_obj
            ).count()
        )

    @pytest.mark.django_db
    def test_add_transaction_invalid(self):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        request_data = {
            'payer': 'Rusty Shackleford',
            'points': -200,
            'timestamp': now
        }

        response = self.web_client.post('/add-transaction/', request_data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.content)
        expected_response = {
            'errors': {'points': ['Cannot transact -200 points. Only 0 are available']},
            'error': True,
            'code': 400,
        }
        self.assertDictEqual(json_response, expected_response)

    @pytest.mark.django_db
    def test_get_balances_all(self):
        PayerBalance.objects.create(
            payer='Rusty Shackleford',
            points=500
        )
        PayerBalance.objects.create(
            payer='Art Vandelay',
            points=1000
        )
        response = self.web_client.get('/get-balance/', content_type='application/json')

        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        expected_response = {
            'success': True,
            'code': 200,
            'results': {
                'Art Vandelay': 1000,
                'Rusty Shackleford': 500
            }
        }
        self.assertDictEqual(json_response, expected_response)

    @pytest.mark.django_db
    def test_get_balances_filtered(self):
        PayerBalance.objects.create(
            payer='Rusty Shackleford',
            points=500
        )
        PayerBalance.objects.create(
            payer='Art Vandelay',
            points=1000
        )

        request_data = {
            'payer': 'Art Vandelay'
        }
        response = self.web_client.get('/get-balance/', request_data, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        expected_response = {
            'success': True,
            'code': 200,
            'results': {
                'Art Vandelay': 1000,
            }
        }
        self.assertDictEqual(json_response, expected_response)

    @pytest.mark.django_db
    def test_spend_points(self):
        datetime_obj = datetime(year=2021, month=3, day=31, hour=10, minute=20, second=30)
        datetime_obj_one_day = datetime_obj + timedelta(days=1)
        datetime_obj_two_day = datetime_obj + timedelta(days=2)

        Transaction.objects.create(
            payer='Rusty Shackleford',
            points=1000,
            timestamp=datetime_obj_two_day,
        )
        Transaction.objects.create(
            payer='Art Vandelay',
            points=400,
            timestamp=datetime_obj,
        )
        Transaction.objects.create(
            payer='Rusty Shackleford',
            points=300,
            timestamp=datetime_obj_one_day,
        )
        Transaction.objects.create(
            payer='Art Vandelay',
            points=-200,
            timestamp=datetime_obj_two_day,
        )

        request_data = {
            'points': 500
        }

        response = self.web_client.post('/spend-points/', request_data, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        expected_response = {
            'success': True,
            'code': 200,
            'results': [
                {
                    'payer': 'Art Vandelay',
                    'points': -200
                },
                {
                    'payer': 'Rusty Shackleford',
                    'points': -300
                }
            ]
        }
        self.assertDictEqual(json_response, expected_response)

    @pytest.mark.django_db
    def test_spend_points_invalid(self):
        datetime_obj = datetime(year=2021, month=3, day=31, hour=10, minute=20, second=30)

        Transaction.objects.create(
            payer='Rusty Shackleford',
            points=100,
            timestamp=datetime_obj,
        )

        request_data = {
            'points': 200
        }

        response = self.web_client.post('/spend-points/', request_data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.content)
        expected_response = {
            'errors': {'points': ['Cannot spend 200 points. Only 100 are available']},
            'error': True,
            'code': 400,
        }
        self.assertDictEqual(json_response, expected_response)

    def test_end_to_end_transaction_balance_spend(self):
        datetime_obj = datetime(year=2021, month=3, day=31, hour=10, minute=20, second=30)
        datetime_obj = pytz.utc.localize(datetime_obj)

        request_data_1 = {
            'payer': 'Rusty Shackleford',
            'points': 100,
            'timestamp': datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        request_data_2 = {
            'payer': 'Art Vandelay',
            'points': 200,
            'timestamp': (datetime_obj + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        request_data_3 = {
            'payer': 'Rusty Shackleford',
            'points': 500,
            'timestamp': (datetime_obj + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        request_data_4 = {
            'payer': 'Rusty Shackleford',
            'points': -200,
            'timestamp': (datetime_obj + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        request_data_5 = {
            'payer': 'Art Vandelay',
            'points': 400,
            'timestamp': (datetime_obj + timedelta(days=4)).strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        # Call to add three transactions
        request_datas = [request_data_1, request_data_2, request_data_3, request_data_4, request_data_5]
        for request_data in request_datas:
            self.web_client.post('/add-transaction/', request_data, content_type='application/json')

        # Get balances that were created by the previous transactions
        balance_response = self.web_client.get('/get-balance/', content_type='application/json')

        self.assertEqual(balance_response.status_code, 200)

        balance_json_response = json.loads(balance_response.content)
        expected_balance_response = {
            'success': True,
            'code': 200,
            'results': {
                'Art Vandelay': 600,
                'Rusty Shackleford': 400
            }
        }
        self.assertDictEqual(balance_json_response, expected_balance_response)

        # Spend points and verify transactions are deducted in the correct order
        spend_request_data = {
            'points': 500
        }

        spend_response = self.web_client.post('/spend-points/', spend_request_data, content_type='application/json')
        spend_json_response = json.loads(spend_response.content)
        expected_spend_response = {
            'success': True,
            'code': 200,
            'results': [
                {
                    'payer': 'Art Vandelay',
                    'points': -200
                },
                {
                    'payer': 'Rusty Shackleford',
                    'points': -300
                }
            ]
        }
        self.assertDictEqual(spend_json_response, expected_spend_response)

        # Get balances again after the first spend
        balance_response_2 = self.web_client.get('/get-balance/', content_type='application/json')

        self.assertEqual(balance_response_2.status_code, 200)

        balance_json_response_2 = json.loads(balance_response_2.content)
        expected_balance_response_2 = {
            'success': True,
            'code': 200,
            'results': {
                'Art Vandelay': 400,
                'Rusty Shackleford': 100
            }
        }
        self.assertDictEqual(balance_json_response_2, expected_balance_response_2)

        # Test an invalid spend amount
        invalid_request_data = {
            'points': 501
        }

        invalid_response = self.web_client.post('/spend-points/', invalid_request_data, content_type='application/json')

        self.assertEqual(invalid_response.status_code, 400)

        invalid_json_response = json.loads(invalid_response.content)
        expected_invalid_response = {
            'errors': {'points': ['Cannot spend 501 points. Only 500 are available']},
            'error': True,
            'code': 400,
        }
        self.assertDictEqual(invalid_json_response, expected_invalid_response)

        # Spend remaining amount
        valid_request_data = {
            'points': 500
        }

        valid_response = self.web_client.post('/spend-points/', valid_request_data, content_type='application/json')

        self.assertEqual(valid_response.status_code, 200)

        valid_json_response = json.loads(valid_response.content)
        expected_valid_response = {
            'success': True,
            'code': 200,
            'results': [
                {
                    'payer': 'Rusty Shackleford',
                    'points': -100
                },
                {
                    'payer': 'Art Vandelay',
                    'points': -400
                }
            ]
        }
        self.assertDictEqual(valid_json_response, expected_valid_response)

        # Get final balances after last spend
        balance_response_final = self.web_client.get('/get-balance/', content_type='application/json')

        self.assertEqual(balance_response_final.status_code, 200)

        balance_json_response_final = json.loads(balance_response_final.content)
        expected_balance_response_final = {
            'success': True,
            'code': 200,
            'results': {
                'Art Vandelay': 0,
                'Rusty Shackleford': 0
            }
        }
        self.assertDictEqual(balance_json_response_final, expected_balance_response_final)
