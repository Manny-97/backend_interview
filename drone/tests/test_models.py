import json
from rest_framework import status
from rest_framework.test import APITestCase

class DroneAPITests(APITestCase):
    drone_url = '/api/drones/'
    medication_url = '/api/v1/medications/'

    def test_empty_fleet(self):

        response = self.client.get(self.drone_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        print(response_data)
        self.assertEqual(0,len(response_data))

    def test_drone_create(self):
        data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 100
        }
        response = self.client.post(self.drone_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        print(response_data)
        self.assertEqual(data['model'], response_data['drone_model'])
        self.assertEqual(data['serial_number'], response_data['serial_number'])
        self.assertEqual(float(data['weight_limit']), float(response_data['weight_limit']))
        
    def test_drone_update(self):
        data = {
            'serial_number': 'drone_01',
            'model': 'Lightweight',
            'weight_limit': 100,
            'battery_capacity': 100
        }
        weight = {'weight_limit': 145}
        response = self.client.post(self.drone_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.assertEqual(float(data['weight_limit']), float(response_data['weight_limit']))
        drone_id = response_data['id']

        response = self.client.patch(path=f"{self.drone_url}{drone_id}/", data=weight, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(float(weight['weight_limit']), float(response_data['weight_limit']))